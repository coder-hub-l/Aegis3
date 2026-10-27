-- ==============================================================================
-- AEGIS3: Star-Graph Common Funder Detection (Gas Dispersal Analysis)
-- Target Platform: Dune Analytics (DuneSQL Engine)
-- Description: Identifies master funder wallets that distribute initial gas ETH
--              to 20+ fresh child wallets within a narrow 48-hour time window.
-- ==============================================================================

WITH gas_funding_transfers AS (
    SELECT 
        "from" AS funder_address,
        "to" AS recipient_wallet,
        value / 1e18 AS eth_amount,
        block_time,
        date_trunc('day', block_time) AS funding_day
    FROM arbitrum.traces
    WHERE call_type = 'call'
      AND success = true
      -- Typical airdrop bot gas funding ranges between 0.003 and 0.08 ETH
      AND value >= 0.003 * 1e18
      AND value <= 0.08 * 1e18
      -- Filter to a 3-month sample window
      AND block_time >= TIMESTAMP '2023-06-01 00:00:00'
      AND block_time <= TIMESTAMP '2023-09-01 00:00:00'
),

funder_aggregation AS (
    SELECT 
        funder_address,
        funding_day,
        COUNT(DISTINCT recipient_wallet) AS wallets_funded_count,
        ROUND(AVG(eth_amount), 4) AS avg_eth_per_wallet,
        ROUND(STDDEV(eth_amount), 6) AS eth_variance,
        MIN(block_time) AS first_transfer_time,
        MAX(block_time) AS last_transfer_time
    FROM gas_funding_transfers
    -- Exclude common central exchanges/bridges if known, or filter high fan-out
    GROUP BY funder_address, funding_day
    HAVING COUNT(DISTINCT recipient_wallet) >= 20
)

SELECT 
    f.funder_address,
    f.funding_day,
    f.wallets_funded_count,
    f.avg_eth_per_wallet,
    f.eth_variance,
    -- Time delta in minutes to fund all wallets in the batch
    date_diff('minute', f.first_transfer_time, f.last_transfer_time) AS batch_duration_minutes
FROM funder_aggregation f
-- An automated script funds wallets with nearly zero variance in ETH amount
WHERE f.eth_variance < 0.001
ORDER BY f.wallets_funded_count DESC
LIMIT 50;
