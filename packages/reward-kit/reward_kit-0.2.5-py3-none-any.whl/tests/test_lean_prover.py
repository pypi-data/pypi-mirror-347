import pytest
from reward_kit.rewards.lean_prover import (
    lean_prover_reward,
    deepseek_prover_v2_reward,
    deepseek_huggingface_prover_benchmark,
)
from reward_kit.models import Message # Import Message

# Helper to create messages list
def create_messages(statement_content: str, assistant_response: str):
    return [
        Message(role="user", content=f"Prove the following statement: {statement_content}"),
        Message(role="assistant", content=assistant_response),
    ]

def test_lean_prover_reward_empty():
    """Test lean_prover_reward with empty input"""
    # Pass empty messages list, or messages with empty content
    messages_empty_assistant = create_messages("some statement", "")
    result = lean_prover_reward(messages=messages_empty_assistant, statement="some statement")
    assert "score" in result
    assert result['score'] == 0.0

    messages_no_assistant = [Message(role="user", content="Prove something")]
    result_no_assistant = lean_prover_reward(messages=messages_no_assistant, statement="something")
    assert "score" in result_no_assistant
    assert result_no_assistant['score'] == 0.0
    
    result_no_statement = lean_prover_reward(messages=messages_empty_assistant, statement=None)
    assert "score" in result_no_statement
    assert result_no_statement['score'] == 0.0


def test_lean_prover_reward_basic():
    """Test lean_prover_reward with a basic example"""
    statement = "All even integers greater than 2 can be expressed as the sum of two primes."
    response = """theorem goldbach (n : ℕ) (h1 : n > 2) (h2 : even n) : ∃ p q, prime p ∧ prime q ∧ p + q = n :=
begin
  sorry
end
    """
    messages = create_messages(statement, response)
    result = lean_prover_reward(messages=messages, statement=statement)
    assert "score" in result

    # Get completeness score from metrics if available
    if "metrics" in result and "completeness" in result['metrics']:
        assert result['metrics']["completeness"]['score'] < 1.0  # Should detect "sorry"


def test_lean_prover_reward_complete():
    """Test lean_prover_reward with a complete proof"""
    statement = "If n is a natural number, then n + 1 > n."
    response = """theorem n_lt_n_plus_one (n : ℕ) : n < n + 1 :=
begin
  apply Nat.lt_succ_self,
end
    """
    messages = create_messages(statement, response)
    result = lean_prover_reward(messages=messages, statement=statement)
    assert "score" in result
    assert result['score'] >= 0.5


def test_lean_prover_reward_verbose():
    """Test verbose output of lean_prover_reward"""
    statement = "If n is a natural number, then n + 1 > n."
    response = """theorem n_lt_n_plus_one (n : ℕ) : n < n + 1 :=
begin
  apply Nat.lt_succ_self,
end
    """
    messages = create_messages(statement, response)
    result = lean_prover_reward(messages=messages, statement=statement, verbose=True)
    assert "score" in result
    assert "metrics" in result
    assert "syntax" in result['metrics']
    assert result['metrics']["syntax"]['score'] > 0


def test_deepseek_prover_v2_reward():
    """Test deepseek_prover_v2_reward with a sample containing subgoals"""
    statement = "For all natural numbers n, the sum of the first n natural numbers is n(n+1)/2."
    response = """theorem sum_naturals (n : ℕ) : ∑ i in range n, i = n * (n + 1) / 2 :=
begin
  -- We'll prove this by induction on n
  induction n with d hd,
  -- Base case: n = 0
  { simp, },
  -- Inductive step: assume true for n = d, prove for n = d + 1
  { 
    have step1 : ∑ i in range (d + 1), i = (∑ i in range d, i) + d,
      by simp [sum_range_succ],
    have step2 : (∑ i in range d, i) + d = d * (d + 1) / 2 + d,
      by rw [hd],
    have step3 : d * (d + 1) / 2 + d = (d * (d + 1) + 2 * d) / 2,
      by ring,
    calc
      ∑ i in range (d + 1), i = (∑ i in range d, i) + d : by simp [sum_range_succ]
      ... = d * (d + 1) / 2 + d : by rw [hd]
      ... = (d * (d + 1) + 2 * d) / 2 : by ring
      ... = (d + 1) * ((d + 1) + 1) / 2 : by ring,
  }
end
    """
    messages = create_messages(statement, response)
    result = deepseek_prover_v2_reward(messages=messages, statement=statement, verbose=True)
    assert "score" in result
    assert result['score'] > 0.7  # Should be high due to good subgoals

    # Check for subgoal analysis in metrics
    assert "metrics" in result
    assert "subgoal_decomposition" in result['metrics']
    assert "hierarchical_structure" in result['metrics']


@pytest.mark.skip(
    reason="Requires Hugging Face datasets package and internet access"
)
def test_deepseek_huggingface_prover_benchmark_mock():
    """Test deepseek_huggingface_prover_benchmark with mocked dataset"""
    statement = "If a and b are positive real numbers, then the arithmetic mean is greater than or equal to the geometric mean."
    response = """theorem AM_GM {a b : ℝ} (ha : 0 < a) (hb : 0 < b) : (a + b) / 2 ≥ sqrt (a * b) :=
begin
  have key : (a - b)^2 ≥ 0,
    by apply pow_two_nonneg,
  have step1 : a^2 - 2*a*b + b^2 ≥ 0,
    by simpa [sq] using key,
  have step2 : a^2 + 2*a*b + b^2 ≥ 4*a*b,
    by linarith,
  have step3 : (a + b)^2 ≥ 4*a*b,
    by simpa [sq] using step2,
  have step4 : (a + b)^2 / 4 ≥ a*b,
    by { apply div_le_div_of_le; linarith; apply step3 },
  have step5 : (a + b) / 2 ≥ sqrt (a * b),
    by { apply le_of_sq_le_sq; apply sqrt_nonneg; apply div_nonneg; 
         apply add_nonneg; apply le_of_lt ha; apply le_of_lt hb; norm_num; 
         rwa [sq_sqrt (mul_nonneg (le_of_lt ha) (le_of_lt hb)), sq_div, sq] },
  exact step5,
end
    """
    messages = create_messages(statement, response)
    dataset_item = {
        "id": "AM_GM_inequality",
        "statement": "If a and b are positive real numbers, then the arithmetic mean is greater than or equal to the geometric mean.",
        "expected_proof": None,
        "reference_solution": "theorem AM_GM {a b : ℝ} (ha : 0 < a) (hb : 0 < b) : (a + b) / 2 ≥ sqrt (a * b)",
    }

    try:
        result = deepseek_huggingface_prover_benchmark(
            messages=messages, statement=statement, dataset_item=dataset_item, verbose=True
        )
        assert "score" in result
        assert result['score'] >= 0.8  # Should be high for good proof
    except ImportError:
        pytest.skip("Hugging Face datasets package not installed")
