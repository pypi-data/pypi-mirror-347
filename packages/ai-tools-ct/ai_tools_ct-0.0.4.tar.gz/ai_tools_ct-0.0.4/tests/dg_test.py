import pytest
import pandas as pd
from unittest.mock import MagicMock
from src.ai_tools_ct.data_generator import DataGenerator 
from src.ai_tools_ct.gpt import Gpt 
from unittest.mock import patch


@pytest.fixture
def mock_gpt():
    """Fixture to mock the Gpt instance and its response."""
    gpt_mock = MagicMock(spec=Gpt)
    gpt_mock.run.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Generated response"))]
    )
    gpt_mock.system_prompt = "default system prompt"
    return gpt_mock


class TestDataGenerator:

    def test_initialization(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        assert isinstance(gen.gpt, Gpt)
        assert gen.generation_results == []

    def test_single_generation_appends_result(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        gen.single_generation(prompt="Say something", target="Greeting", system_prompt="Be nice")

        results = gen.generation_results
        assert len(results) == 1
        assert results[0]["GPT prompt"] == "Say something"
        assert results[0]["Result"] == "Generated response"
        assert results[0]["Target (optional)"] == "Greeting"
        mock_gpt.run.assert_called_once_with("Say something")
        assert gen.df_generation_results.shape[0] == 1

    def test_bulk_generation_basic(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        prompts = ["prompt 1", "prompt 2"]
        targets = ["target 1", "target 2"]

        gen.bulk_generation(prompts=prompts, targets=targets)

        results = gen.generation_results
        assert len(results) == 2
        assert results[0]["GPT prompt"] == "prompt 1"
        assert results[1]["Target (optional)"] == "target 2"

    def test_bulk_generation_with_system_prompts(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        prompts = ["what is AI?", "explain gravity"]
        system_prompts = ["Talk like a teacher", "Talk like a scientist"]

        gen.bulk_generation(prompts=prompts, system_prompts=system_prompts)

        assert mock_gpt.system_prompt == "Talk like a scientist"
        assert gen.df_generation_results.shape[0] == 2

    def test_bulk_generation_invalid_prompts_type(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        with pytest.raises(ValueError, match="prompts must be a list of strings"):
            gen.bulk_generation(prompts="not a list")

    def test_bulk_generation_mismatched_targets(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        with pytest.raises(ValueError, match="targets must match length of prompts"):
            gen.bulk_generation(prompts=["a", "b"], targets=["only one"])

    def test_bulk_generation_mismatched_system_prompts(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        with pytest.raises(ValueError, match="system_prompts must match length of prompts"):
            gen.bulk_generation(prompts=["a", "b"], system_prompts=["only one"])
    
    def test_generation_results_returns_copy(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)

        # Generate one result
        gen.single_generation(prompt="Hello", target="Greeting")

        results = gen.generation_results
        assert isinstance(results, list)
        assert len(results) == 1
        assert results[0]["GPT prompt"] == "Hello"

        # Modify the returned list – it should not affect the original
        results.append({"GPT prompt": "Fake", "Result": "Bad", "Target (optional)": "Oops"})
        assert len(results) == 2
        assert len(gen.generation_results) == 1  # Still 1 internally

    def test_df_generation_results_format(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)

        gen.single_generation(prompt="What is AI?", target="Definition")
        df = gen.df_generation_results

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert set(df.columns) == {"GPT prompt", "Result", "Target (optional)"}
        assert df.iloc[0]["GPT prompt"] == "What is AI?"

    def test_parallel_generation_basic(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        prompts = ["prompt 1", "prompt 2", "prompt 3"]

        gen.parallel_generation(prompts=prompts)

        results = gen.generation_results
        assert len(results) == 3

        # since order is not guaranteed in parallel generation, we use set to compare
        generated_prompts = {r["GPT prompt"] for r in results}
        assert set(prompts) == generated_prompts

    def test_parallel_generation_with_targets(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        prompts = ["prompt 1", "prompt 2"]
        targets = ["target 1", "target 2"]

        gen.parallel_generation(prompts=prompts, targets=targets)

        results = gen.generation_results
        assert len(results) == 2

        # Make sure prompt-target mapping is correct
        mapping = {r["GPT prompt"]: r["Target (optional)"] for r in results}

        for prompt, target in zip(prompts, targets):
            assert mapping[prompt] == target

    def test_parallel_generation_with_system_prompts(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        prompts = ["what is AI?", "explain gravity"]
        system_prompts = ["Talk like a teacher", "Talk like a scientist"]

        gen.parallel_generation(prompts=prompts, system_prompts=system_prompts)

        assert gen.df_generation_results.shape[0] == 2
        assert all(col in gen.df_generation_results.columns for col in ["GPT prompt", "Result", "Target (optional)"])

    def test_parallel_generation_invalid_prompts_type(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        with pytest.raises(ValueError, match="prompts must be a list of strings"):
            gen.parallel_generation(prompts="not a list")

    def test_parallel_generation_mismatched_targets(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        with pytest.raises(ValueError, match="targets must match length of prompts"):
            gen.parallel_generation(prompts=["a", "b"], targets=["only one"])

    def test_parallel_generation_mismatched_system_prompts(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        with pytest.raises(ValueError, match="system_prompts must match length of prompts"):
            gen.parallel_generation(prompts=["a", "b"], system_prompts=["only one"])

    def test_parallel_generation_stress_many_prompts(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        prompts = [f"prompt {i}" for i in range(500)]  # Large number of prompts

        gen.parallel_generation(prompts=prompts)

        results = gen.generation_results
        assert len(results) == 500
        prompts_set = set(r["GPT prompt"] for r in results)
        assert prompts_set == set(prompts)

    def test_parallel_generation_with_different_max_workers(self, mock_gpt):
        gen = DataGenerator(gpt=mock_gpt)
        prompts = ["prompt 1", "prompt 2", "prompt 3", "prompt 4"]

        for workers in [1, 2, 4]:
            gen._generation_results = []  # Reset before each
            gen.parallel_generation(prompts=prompts, max_workers=workers)
            assert len(gen.generation_results) == 4