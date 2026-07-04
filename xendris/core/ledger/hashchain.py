"""Deterministic local hash chain verification logic."""

from __future__ import annotations

from xendris.core.ledger.record import TrustLedgerRecord


class TrustHashChain:
    """Provides verification services for a local deterministic hash chain."""

    @staticmethod
    def verify_chain(records: list[TrustLedgerRecord]) -> bool:
        """Verify that a sequence of records forms a valid, unbroken hash chain."""
        if not records:
            return True

        # Verify first record hash
        if records[0].record_hash != records[0].calculate_record_hash():
            return False

        for i in range(1, len(records)):
            prev = records[i - 1]
            curr = records[i]

            # Verify link to previous record hash
            if curr.previous_record_hash != prev.record_hash:
                return False

            # Verify current record contents match current record hash
            if curr.record_hash != curr.calculate_record_hash():
                return False

        return True
