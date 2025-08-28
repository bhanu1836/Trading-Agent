// This file manages background processes for the extension, such as handling messages between the popup and content scripts.

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "executeCommand") {
        // Handle the command execution logic here
        // For example, you might want to send the command to the content script
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            chrome.tabs.sendMessage(tabs[0].id, { command: request.command }, (response) => {
                sendResponse(response);
            });
        });
        return true; // Indicates that the response will be sent asynchronously
    }
});