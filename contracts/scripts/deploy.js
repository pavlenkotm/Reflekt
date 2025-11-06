// Deployment script for ReputationNFT contract
const hre = require("hardhat");

async function main() {
  console.log("Deploying ReputationNFT contract...");

  // Get the contract factory
  const ReputationNFT = await hre.ethers.getContractFactory("ReputationNFT");

  // Deploy the contract
  const reputationNFT = await ReputationNFT.deploy();

  await reputationNFT.waitForDeployment();

  const address = await reputationNFT.getAddress();

  console.log(`✓ ReputationNFT deployed to: ${address}`);
  console.log(`\nNetwork: ${hre.network.name}`);
  console.log(`Deployer: ${(await hre.ethers.getSigners())[0].address}`);

  // Wait for a few block confirmations before verifying
  if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
    console.log("\nWaiting for block confirmations...");
    await reputationNFT.deploymentTransaction().wait(5);

    console.log("\nVerifying contract on Etherscan...");
    try {
      await hre.run("verify:verify", {
        address: address,
        constructorArguments: [],
      });
      console.log("✓ Contract verified!");
    } catch (error) {
      console.log("Verification error:", error.message);
    }
  }

  // Save deployment info
  const fs = require("fs");
  const deploymentInfo = {
    network: hre.network.name,
    contractAddress: address,
    deployer: (await hre.ethers.getSigners())[0].address,
    timestamp: new Date().toISOString(),
  };

  const outputPath = `../data/deployments/${hre.network.name}.json`;
  fs.mkdirSync("../data/deployments", { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(deploymentInfo, null, 2));

  console.log(`\n✓ Deployment info saved to: ${outputPath}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
