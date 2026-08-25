import json
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address


def ok(receipt):
    assert tx_execution_succeeded(receipt)
    assert receipt.get("status_name") == TransactionStatus.FINALIZED.value
    assert receipt.get("result_name") in (None, "AGREE", "MAJORITY_AGREE")
    assert receipt.get("tx_execution_result_name") in (None, "FINISHED_WITH_RETURN")
    return receipt


@pytest.mark.integration
def test_studionet_feedback_classification(
    default_account, secondary_account, tertiary_account
):
    factory = get_contract_factory(
        contract_file_path=Path(__file__).resolve().parents[2]
        / "contracts"
        / "feedback_theme_board.py"
    )
    deployed = ok(
        factory.deploy_contract_tx(
            args=[
                "What should we improve before the next neighborhood workshop?",
                "Use only the submitted feedback and frozen descriptions to choose the closest theme. Do not infer urgency, emotion, identity, or medical risk.",
            ],
            account=default_account,
            wait_transaction_status=TransactionStatus.FINALIZED,
        )
    )
    address = extract_contract_address(deployed)
    facilitator = factory.build_contract(address, account=default_account)
    participant_two = factory.build_contract(address, account=secondary_account)
    participant_three = factory.build_contract(address, account=tertiary_account)
    ok(
        facilitator.add_theme(
            args=["ACCESS", "Venue access, timing, signage, and arrival instructions."]
        ).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    )
    ok(
        facilitator.add_theme(
            args=["MATERIALS", "Workshop handouts, tools, examples, and learning materials."]
        ).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    )
    ok(
        facilitator.open_feedback(args=[]).transact(
            wait_transaction_status=TransactionStatus.FINALIZED
        )
    )
    ok(
        facilitator.submit_feedback(
            args=[
                "f1",
                "Please put larger direction signs by both entrances because several attendees could not find the evening room.",
            ]
        ).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    )
    ok(
        participant_two.submit_feedback(
            args=[
                "f2",
                "A one-page printed example would make the hands-on exercise easier to follow at the next workshop.",
            ]
        ).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    )
    ok(
        participant_three.submit_feedback(
            args=[
                "f3",
                "Please publish the entrance opening time in advance so guests can plan when to arrive.",
            ]
        ).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    )
    ok(
        facilitator.lock_feedback(args=[]).transact(
            wait_transaction_status=TransactionStatus.FINALIZED
        )
    )
    intelligent = ok(
        facilitator.classify_feedback(args=["f1"]).transact(
            wait_transaction_status=TransactionStatus.FINALIZED
        )
    )
    feedback = facilitator.get_feedback(args=["f1"]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert feedback["assigned_theme"] in ("ACCESS", "MATERIALS", "OTHER")
    observed = {"theme": feedback["assigned_theme"]}
    print(
        "STUDIONET_RECORD="
        + json.dumps(
            {
                "address": address,
                "deploy_tx": deployed["hash"],
                "intelligent_tx": intelligent["hash"],
                "observed": observed,
            },
            sort_keys=True,
        )
    )
