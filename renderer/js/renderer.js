const { ipcRenderer } = require('electron');
const axios = require('axios');
const io = require('socket.io-client');
const socket = io('http://localhost:5000'); // Adjust the URL to your Flask server
const path = require('path');
const fs = require('fs');

document.getElementById('minimize-button').addEventListener('click', () => {
    ipcRenderer.send('minimize-window');
});

document.getElementById('maximize-button').addEventListener('click', () => {
    ipcRenderer.send('maximize-window');
});

document.getElementById('close-button').addEventListener('click', () => {
    ipcRenderer.send('close-window');
});


document.addEventListener('DOMContentLoaded', () => {
    // Get the modal and button
    const modal = document.getElementById('myModal');
    const submitButton = document.getElementById('submit-button');
    
    // Function to handle submit
    submitButton.addEventListener('click', function () {
        const selectedProgram = document.getElementById('program-dropdown').value;
        const selectedTerm = document.getElementById('term-dropdown').value;
        const selectedDate = document.getElementById('start-date').value;

        if (selectedDate) {
            // You can perform an action here with the selected values
            console.log('Term:', selectedProgram);
            console.log('Start Date:', selectedDate);

            // Close the modal
            modal.style.display = 'none';
            document.body.classList.remove('modal-open');
            createTerms(selectedProgram, selectedTerm, selectedDate);
            attachDragEvents();
        } else {
            alert('Please select a date.');
        }
    });
});

socket.on('connect', () => {
    console.log('Connected to the server');
    axios.post('http://127.0.0.1:5000/onStart')
        .then(response => {
            console.log('Conversation started', response.data);
        })
        .catch(error => {
            console.error('Error starting conversation:', error);
        });
});

async function requestCourseDetails(courseName) {
    console.log('Requesting Course information on:', courseName);
    try {
        // Wait for the response from axios
        const response = await axios.post('http://127.0.0.1:5000/courseDetails', { courseName });
        console.log('Response from backend:', response.data);
        return response.data; // Return the actual response data
    } catch (error) {
        console.error('Error sending message to backend:', error);
        return null; // Return null or handle the error appropriately
    }
}

async function requestCourseInformation(courseName, termNumber) {
    console.log('Requesting Course information on:', courseName);
    try {
        // Wait for the response from axios
        const response = await axios.post('http://127.0.0.1:5000/courseInfo', { courseName, termNumber });
        console.log('Response from backend:', response.data);
        return response.data; // Return the actual response data
    } catch (error) {
        console.error('Error sending message to backend:', error);
        return null; // Return null or handle the error appropriately
    }
}

async function getCourseStatus(courseName) {
    console.log('Requesting Course information on:', courseName);
    try {
        // Wait for the response from axios
        const response = await axios.post('http://127.0.0.1:5000/courseStatus', { courseName });
        console.log('Response from backend:', response.data);
        return response.data; // Return the actual response data
    } catch (error) {
        console.error('Error sending message to backend:', error);
        return null; // Return null or handle the error appropriately
    }
}

async function removeCourse(courseName) {
    console.log('Requesting Course information on:', courseName);
    try {
        // Wait for the response from axios
        const response = await axios.post('http://127.0.0.1:5000/removeCourse', { courseName });
        console.log('Response from backend:', response.data);
        return response.data; // Return the actual response data
    } catch (error) {
        console.error('Error sending message to backend:', error);
        return null; // Return null or handle the error appropriately
    }
}


const courseCardTemplate = document.getElementById('course-card-template').content

// Get the term template
const termTemplate = document.getElementById('term-template').content;

// Function to generate terms dynamically
function createTerms(selectedProgram, selectedTerm, selectedYear) {
    const container = document.getElementById('terms-container'); // Get the container for terms
    
     // Define the term labels in order
    const termLabels = ["Winter", "Spring", "Summer", "Fall"];

    // Determine the starting term index based on the selected term
    let startTermIndex = termLabels.indexOf(selectedTerm);

    // Initialize an array to store the generated terms
    const terms = [];

    // Determine how many terms to generate based on the selected program (4 years or 5 years)
    var totalTerms = selectedProgram === "FourYear" ? 16 : 20;
    totalTerms+=1;

    // Generate the terms starting from the selected term and year
    let currentYear = selectedYear;
    for (let i = 0; i < totalTerms; i++) {
        // Get the term label based on the start term index
        const termLabel = termLabels[startTermIndex];

        // Push the generated term to the terms array with a default credit value
        if (i === 0) {
            terms.push({ title: `${"Pre College"}<br>${parseInt(currentYear) - 1}`, credits: '0.0 / 20.0' });
        }
        terms.push({ title: `${termLabel}<br>${currentYear}`, credits: '0.0 / 20.0' });

        // Increment the term index and handle wrapping around the terms
        startTermIndex = (startTermIndex + 1) % 4;

        // If the term wraps back to "Winter", increment the year
        if (startTermIndex === 0) {
            currentYear++;
        }
    }

    // Generate 20 terms dynamically
    for (let i = 0; i < totalTerms; i++) {
        // Clone the template
        const termElement = document.importNode(termTemplate, true);
        termElement.querySelector('.term-div').id = `term-${i}`;

        // Assign dynamic data to the term
        const termData = terms[i % terms.length]; // Loop through sample term data for the example
        termElement.querySelector('.term-title').innerHTML = `${termData.title}`; // Dynamic term name
        termElement.querySelector('.term-credits').textContent = termData.credits; // Dynamic term credits

        // Optionally, you can generate courses within each term using the same course generation logic here.
        const coursesContainer = termElement.querySelector('.courses-container');
        coursesContainer.id = `courses-container-${i}`;  // Dynamic ID based on termIndex


        // Append the term to the container
        container.appendChild(termElement);
    }
}

function createCourseCards() {
    // Define an array of course data for the 7 courses
    const courses = [
      { shortName: "CS 265", credits: 3.0, status: "checkmark" },
      { shortName: "CS 201", credits: 4.0, status: "warning" },
      { shortName: "CS 301", credits: 3.0, status: "error" },
      { shortName: "CS 351", credits: 3.0, status: "checkmark" },
      { shortName: "CS 354", credits: 3.0, status: "warning" },
      { shortName: "CS 432", credits: 3.0, status: "error" },
      { shortName: "MATH 101", credits: 4.0, status: "checkmark" },
    ];
  
    // Get the container where the course cards will be inserted
    const container = document.getElementById("courses-container-1");
  
    // Iterate through the courses array and create each card
    courses.forEach(course => {
        container.appendChild(createCourseObject(course));
    });
}

function createCourseObject(course) {
    const courseCard = document.importNode(courseCardTemplate, true);
  
      // Update the course name
      courseCard.querySelector(".course-name").textContent = course.shortName;
  
      // Update the course credits
      courseCard.querySelector(".course-credits").textContent = `${course.credits} credits`;

      const statusIcon = document.createElement('i');
      statusIcon.classList.add('status-icon');
  
      // Update the icon and status
      if (course.status === "checkmark") {
        statusIcon.textContent = "✔"; // Checkmark icon
        statusIcon.classList.add("checkmark"); // Apply checkmark styling
      } else if (course.status === "warning") {
        statusIcon.textContent = "⚠"; // Warning icon
        statusIcon.classList.add("warning"); // Apply warning styling
      } else if (course.status === "error") {
        statusIcon.textContent = "✘"; // X icon
        statusIcon.classList.add("error"); // Apply error styling
      }

      // Append the status icon at the correct place in the course card
      const courseCardContainer = courseCard.querySelector('.course-card');
      courseCardContainer.appendChild(statusIcon);  // Append it inside the course-card

      return courseCard
}