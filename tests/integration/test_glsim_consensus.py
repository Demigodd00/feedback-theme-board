from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Score one feedback entry"


def context(theme_scores):
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"theme_scores": theme_scores})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_feedback_priority_board():
    facilitator_account, second_account, third_account = create_accounts(3)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "feedback_theme_board.py")
    deployed = factory.deploy_contract_tx(args=["What should the community workshop improve for the next monthly session?", "Use only the submitted feedback and frozen descriptions to choose the closest theme. Do not infer urgency, emotion, identity, or medical risk."], account=facilitator_account, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    contract_address = extract_contract_address(deployed)
    facilitator = factory.build_contract(contract_address, account=facilitator_account)
    second = factory.build_contract(contract_address, account=second_account)
    third = factory.build_contract(contract_address, account=third_account)
    ok(facilitator.add_theme(args=["ACCESS", "Room entry, seating, and physical setup for participants."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(facilitator.add_theme(args=["MATERIALS", "Handouts, tools, and examples used during the workshop."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(facilitator.open_feedback(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(facilitator.submit_feedback(args=["f1", "The side-door code expires Friday, so a new code must be sent before Saturday's workshop."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(second.submit_feedback(args=["f2", "The exercise sheet should include one complete worked example before the next session."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(third.submit_feedback(args=["f3", "A larger sign near the side entrance would make the regular arrival route easier to spot."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(facilitator.lock_feedback(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(facilitator.classify_feedback(args=["f1"]).transact(transaction_context=context("20"), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(facilitator.classify_feedback(args=["f2"]).transact(transaction_context=context("02"), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(facilitator.classify_feedback(args=["f3"]).transact(transaction_context=context("20"), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(facilitator.vote_priority(args=["ACCESS"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(second.vote_priority(args=["ACCESS"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(facilitator.finalize_board(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    state = facilitator.get_state(args=[]).call()
    assert state["priority_theme"] == "ACCESS"
    assert state["priority_quorum"] == 2
    assert state["nonvoter_count"] == 1
