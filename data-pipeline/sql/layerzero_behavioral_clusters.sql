-- ==============================================================================
-- AEGIS3: LayerZero Sybil Cluster Detection via Behavioral Footprinting
-- Target Platform: Dune Analytics (DuneSQL Engine)
-- Description: Groups candidate airdrop wallets that exhibit identical interaction 
--              footprints (exact tx count, active days, and chain bitmask pathways).
-- ==============================================================================

WITH lz_wallet_summary AS (
    SELECT 
        user_address,
        COUNT(*) AS total_transactions,
        CAST(date_trunc('day', MIN(block_time)) AS DATE) AS first_active_day,
        CAST(date_trunc('day', MAX(block_time)) AS DATE) AS last_active_day,
        COUNT(DISTINCT date_trunc('day', block_time)) AS distinct_active_days,
        
        -- Chain bitmask: Identifies the exact combination of source chains used
        0 + IF(bool_or(source_chain_name = 'Optimism'), 1, 0)
          + IF(bool_or(source_chain_name = 'Arbitrum'), 2, 0)
          + IF(bool_or(source_chain_name = 'Ethereum'), 4, 0)
          + IF(bool_or(source_chain_name = 'Polygon'), 8, 0)
          + IF(bool_or(source_chain_name = 'BNB Chain'), 16, 0)
          + IF(bool_or(source_chain_name = 'Avalanche'), 32, 0)
          + IF(bool_or(source_chain_name = 'Base'), 64, 0) 
        AS source_chains_bitmask

    FROM layerzero.send
    -- Focus on the main LayerZero snapshot activity window
    WHERE block_time >= TIMESTAMP '2023-01-01 00:00:00'
      AND block_time <= TIMESTAMP '2024-05-01 00:00:00'
    GROUP BY user_address
),

sybil_clusters AS (
    SELECT 
        total_transactions,
        first_active_day,
        last_active_day,
        distinct_active_days,
        source_chains_bitmask,
        COUNT(*) AS cluster_size,
        -- Collect up to 50 wallet addresses per cluster for analysis
        array_agg(user_address) AS wallet_addresses
    FROM lz_wallet_summary
    WHERE total_transactions >= 3  -- Filter out 1-time accidental bridge users
    GROUP BY 
        total_transactions,
        first_active_day,
        last_active_day,
        distinct_active_days,
        source_chains_bitmask
)

-- Return clusters containing 15 or more synchronized wallets
SELECT 
    cluster_size,
    first_active_day,
    last_active_day,
    distinct_active_days,
    total_transactions,
    source_chains_bitmask,
    wallet_addresses
FROM sybil_clusters
WHERE cluster_size >= 15
ORDER BY cluster_size DESC
LIMIT 100;
