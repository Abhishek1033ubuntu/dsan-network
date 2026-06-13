// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title DSAN Verifiable Demand Commitment (VDC) Escrow
 * @notice Implements Tier 1 macroeconomic stabilization by locking importer collateral 
 * and automating milestone-based cross-border settlements via telemetric triggers.
 */
contract VDCEscrow {
    
    address public globalGovernanceAdmin;
    uint256 public constant BUFFER_THRESHOLD = 15; // 15% algorithmic volatility buffer (σ_buffer)
    uint256 public movingAveragePrice;             // P_MA (scaled to 6 decimals, e.g., $250.00 = 250000000)

    struct DemandCommitment {
        address importer;
        uint256 demandVolume;    // D_k (in metric tons)
        uint256 lockedCollateral; // V_escrow (in Wei or mock stablecoin units)
        bool telemetryVerified;   // F_C status passed from Tier 2 Gateway
        bool customsCleared;      // Ψ_SPS milestone (30% payout trigger)
        bool geofenceBreached;    // Γ_geo milestone (70% final settlement trigger)
        bool isSettled;
    }

    mapping(bytes32 => DemandCommitment) public commitments;

    event CommitmentCreated(bytes32 indexed commitmentId, address indexed importer, uint256 volume, uint256 collateralLocked);
    event TelemetryPassed(bytes32 indexed commitmentId);
    event MilestoneTriggered(bytes32 indexed commitmentId, string milestoneType, uint256 amountReleased);
    event SettlementCompleted(bytes32 indexed commitmentId);

    modifier onlyAdmin() {
        require(msg.sender == globalGovernanceAdmin, "DSAN: Auth failure - Only Global Core admin permitted");
        _;
    }

    constructor(uint256 _initialPrice) {
        globalGovernanceAdmin = msg.sender;
        movingAveragePrice = _initialPrice;
    }

    /**
     * @notice Tier 1 Step 1: Importer registers demand and locks required collateral plus volatility buffer.
     * @param _commitmentId Unique cryptographic tracking hash for the global trade route.
     * @param _volume Target grain/crop volume requested in metric tons (D_k).
     */
    function createDemandCommitment(bytes32 _commitmentId, uint256 _volume) external payable {
        require(commitments[_commitmentId].importer == address(0), "DSAN: Commitment ID already exists");
        require(_volume > 0, "DSAN: Volume must exceed zero");

        // Mathematical Evaluation: V_escrow = (D_k * P_MA) * (1 + σ_buffer)
        uint256 baseValue = _volume * movingAveragePrice;
        uint256 bufferValue = (baseValue * BUFFER_THRESHOLD) / 100;
        uint256 requiredEscrow = baseValue + bufferValue;

        require(msg.value >= requiredEscrow, "DSAN: Insufficient collateral lock payload");

        commitments[_commitmentId] = DemandCommitment({
            importer: msg.sender,
            demandVolume: _volume,
            lockedCollateral: msg.value,
            telemetryVerified: false,
            customsCleared: false,
            geofenceBreached: false,
            isSettled: false
        });

        emit CommitmentCreated(_commitmentId, msg.sender, _volume, msg.value);
    }

    /**
     * @notice Tier 2 Ingestion: Autonomous Gateway oracle submits verified satellite telemetry proof.
     */
    function verifyTelemetry(bytes32 _commitmentId) external onlyAdmin {
        DemandCommitment storage commitment = commitments[_commitmentId];
        require(commitment.importer != address(0), "DSAN: Target commitment profile not found");
        
        commitment.telemetryVerified = true;
        emit TelemetryPassed(_commitmentId);
    }

    /**
     * @notice Cross-Border Settlement: Validates milestones and routes automated distributions to exporters.
     * @dev Implements binary vector logic: D_payout = [γ1 * Ψ_SPS + γ2 * Γ_geo] x V_escrow
     */
    function processMilestonePayout(bytes32 _commitmentId, address payable _exporter, uint8 _milestoneStage) external onlyAdmin {
        DemandCommitment storage commitment = commitments[_commitmentId];
        require(commitment.telemetryVerified, "DSAN: Settlement blocked - Telemetry verification (F_C) pending");
        require(!commitment.isSettled, "DSAN: Trade route already fully liquidated");

        uint256 totalCollateral = commitment.lockedCollateral;

        if (_milestoneStage == 1 && !commitment.customsCleared) {
            // Milestone 1 (Ψ_SPS): Custom clearance verified at origin terminal. Release 30% (γ1).
            commitment.customsCleared = true;
            uint256 payout1 = (totalCollateral * 30) / 100;
            _exporter.transfer(payout1);
            emit MilestoneTriggered(_commitmentId, "SPS_CUSTOMS_CLEARED", payout1);
        } 
        else if (_milestoneStage == 2 && !commitment.geofenceBreached) {
            // Milestone 2 (Γ_geo): Satellite AIS tracking detects vessel breaching destination geofence. Release remaining 70% (γ2).
            require(commitment.customsCleared, "DSAN: Milestones must execute sequentially");
            commitment.geofenceBreached = true;
            commitment.isSettled = true;
            
            uint256 payout2 = address(this).balance; // Clear out remaining balance including safety buffer refunds
            _exporter.transfer(payout2);
            
            emit MilestoneTriggered(_commitmentId, "GEOFENCE_DESTINATION_BREACHED", payout2);
            emit SettlementCompleted(_commitmentId);
        }
    }

    /**
     * @notice Dynamic Oracle Feed: Updates moving average spot price based on global network equilibrium.
     */
    function updateMovingAveragePrice(uint256 _newPrice) external onlyAdmin {
        movingAveragePrice = _newPrice;
    }
}