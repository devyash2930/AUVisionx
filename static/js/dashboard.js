// dashboard.js

document.addEventListener('DOMContentLoaded', function () {
    // Assuming the user role is set in the backend, you can use it to determine options
    const isStudent = true;  // Replace with the actual user role from the backend

    const optionsContainer = document.getElementById("options-container");

    if (isStudent) {
        // Display student options
        displayStudentOptions(optionsContainer);
    } else {
        // Display admin options
        displayAdminOptions(optionsContainer);
    }

    // Add an event listener to the Start Server button
    document.getElementById('startServer').addEventListener('click', function () {
        // Execute the shell command to start the server
        executeShellCommand('npx http-server');
    });
});

// Function to execute shell commands
function executeShellCommand(command) {
    // Create an XMLHttpRequest object
    var xhr = new XMLHttpRequest();

    // Configure it as a GET request to a special endpoint that triggers shell commands
    xhr.open('GET', '/run-command?command=' + encodeURIComponent(command), true);

    // Send the request
    xhr.send();
}

function displayStudentOptions(container) {
    const studentOptions = ["Enroll Courses", "View Enrolled Courses"];
    displayOptions(container, studentOptions);
}

function displayAdminOptions(container) {
    const adminOptions = ["Add Courses", "Delete Courses", "Modify Courses"];
    displayOptions(container, adminOptions);
}

function displayOptions(container, options) {
    options.forEach(option => {
        const button = document.createElement("button");
        button.className = "options-button";
        button.textContent = option;
        container.appendChild(button);

        button.addEventListener("click", function () {
            // Handle button click based on the selected option
            console.log(`Clicked on: ${option}`);
        });
    });
}

