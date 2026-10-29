console.log("Aegis3 Initializing Transaction Shield...");

// Helper function to wrap window.ethereum
function installWiretap() {
    if (!window.ethereum || window.ethereum.__aegis3_installed) {
        return;
    }

    const originalRequest = window.ethereum.request.bind(window.ethereum);

    window.ethereum.request = async function(args) {
        console.log("Aegis3 Caught Method:", args.method, args.params);

        // Check if this is a transaction or token permit signature
        if (args.method === "eth_sendTransaction") {
            const proceed = confirm("Aegis3 Alert: A site is trying to send a transaction! Do you want to allow this to reach MetaMask?");
            if (!proceed) {
                // Reject it right here! MetaMask will never even see it.
                throw { code: 4001, message: "Transaction blocked by Aegis3 Shield." };
            }
        }

        // If safe or approved, forward it to the real MetaMask
        return originalRequest(args);
    };

    window.ethereum.__aegis3_installed = true;
    console.log("Aegis3 Wiretap successfully attached to window.ethereum!");
}

// Since MetaMask might inject window.ethereum slightly after page start,
// we listen for Ethereum provider injection:
if (window.ethereum) {
    installWiretap();
} else {
    window.addEventListener("ethereum#initialized", installWiretap, { once: true });
}