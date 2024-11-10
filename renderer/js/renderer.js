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

document.getElementById('save-button').addEventListener('click', async () => {
    try {
        // Get current date in YYYYMMDD format
        const today = new Date();
        const currentDate = `${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, '0')}${String(today.getDate()).padStart(2, '0')}`;
        
        // Set default filename with date and last name
        const options = {
            suggestedName: `${currentDate}_oldweiler_.json`, 
            types: [{
                description: 'JSON Files',
                accept: { 'application/json': ['.json'] }
            }],
            startIn: 'documents'  // Default location (if supported)
        };
    
        const handle = await window.showSaveFilePicker(options);
        const writable = await handle.createWritable();
        
        // Customize with your JSON data
        const dataToSave = await getSchedule();  // Replace with actual data
        await writable.write(JSON.stringify(dataToSave, null, 2));  // Write as formatted JSON
        await writable.close();
        
        console.log("File saved successfully.");
    } catch (error) {
        console.error("File save was canceled or failed.", error);
    }
    
});

document.getElementById('load-button').addEventListener('click', () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';  // Restrict file type to JSON
    input.style.display = 'none';

    input.addEventListener('change', async (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = async () => {
                try {
                    // Parse the JSON content
                    const jsonData = JSON.parse(reader.result);
                    console.log("File content as JSON:", jsonData);

                    // Replacing the original loop with the fixed one
                    for (const [courseFile, term] of Object.entries(jsonData)) {
                        try {
                            // Await request for course details to ensure correct association with courseFile
                            let courseResponse = await requestCourseDetails(courseFile);
                            let course = courseResponse.courseInfo;

                            // Create a new course card
                            const courseItem = document.importNode(document.getElementById('course-card-template').content, true);
                            const courseItemDiv = courseItem.querySelector('.course-card');

                            // Set course details
                            courseItemDiv.querySelector('.course-name').textContent = course.shortName;
                            courseItemDiv.querySelector('.course-credits').textContent = `${course.courseCredits} credits`;

                            // Add drag and click event listeners
                            courseItem.addEventListener('dragstart', (event) => handleDragStart(event, course));

                            courseItemDiv.addEventListener('click', async () => {
                                const courseDetails = (await requestCourseDetails(course.shortName)).courseInfo;
                                const courseDetailStatus = await getCourseStatus(course.shortName);
                                const dialogDiv = document.querySelector('.dialog-content');

                                dialogDiv.querySelector('.course-name').textContent = courseDetails.fullName;
                                dialogDiv.querySelector('.short-name').textContent = courseDetails.shortName;
                                dialogDiv.querySelector('.course-desc').textContent = "Description: " + courseDetails.courseDesc;
                                dialogDiv.querySelector('.course-prereqs').textContent = "Prerequisites: " + courseDetails.prereqs;
                                dialogDiv.querySelector('.course-coreqs').textContent = "Corequisites: " + courseDetails.coreqs;
                                dialogDiv.querySelector('.course-offered').textContent = "Offered Terms: " + courseDetails.offered;

                                changeStatusIcon(courseDetailStatus, dialogDiv.querySelector('.course-status'));
                                document.querySelector('.course-dialog').showModal();
                            });

                            // Set up drag events
                            courseItemDiv.addEventListener("dragstart", () => {
                                courseItemDiv.classList.add("is-dragging");
                            });
                            courseItemDiv.addEventListener("dragend", async () => {
                                const parentZone = courseItemDiv.closest('.term-div');
                                if (parentZone) {
                                    const courseStatus = await requestCourseInformation(course.shortName, parentZone.id);
                                    const iconElement = courseItemDiv.querySelector('.status-icon');
                                    changeStatusIcon(courseStatus, iconElement);
                                }
                                updateCourseStatus();
                                updateTermCredits();
                                courseItemDiv.classList.remove("is-dragging");
                            });

                            // Add status icon
                            courseCardList.push(courseItemDiv)
                            const statusIcon = document.createElement('i');
                            statusIcon.classList.add('status-icon');
                            statusIcon.textContent = "✔";
                            statusIcon.classList.add("checkmark");
                            courseItemDiv.appendChild(statusIcon);

                            // Append course to the appropriate term container
                            const addedContainer = document.getElementById(`courses-container-${term}`);
                            addedContainer.appendChild(courseItemDiv);

                            console.log("---------------------------")

                            const courseStatus = await requestCourseInformation(course.shortName, `term-${term}`);
                            const iconElement = courseItemDiv.querySelector('.status-icon');
                            changeStatusIcon(courseStatus, iconElement);
                            updateCourseStatus();
                            updateTermCredits();

                        } catch (error) {
                            console.error("Failed to load course details:", error);
                        }
                    }
                } catch (error) {
                    console.error("Failed to parse JSON file:", error);
                }
            };
            reader.readAsText(file);
        }
    });

    document.body.appendChild(input);
    input.click();
    document.body.removeChild(input);
});



async function updateCourseStatus() {
    for (const courseElement of courseCardList) {
      var shortName = courseElement.querySelector('.course-name').textContent;
      var courseStatus = await getCourseStatus(shortName)
      const iconElement = courseElement.querySelector('.status-icon');
      changeStatusIcon(courseStatus, iconElement)
    }
  }

  function updateTermCredits() {
    // Get all the term divs
    const allTermDivs = document.querySelectorAll('.term-div');
  
    allTermDivs.forEach(termDiv => {
        // Get the courses container for this term
        const coursesContainer = termDiv.querySelector('.courses-container');
  
        // Initialize the total credits for this term
        let totalCredits = 0;
  
        // Loop through each course-card in the courses container
        const courseCards = coursesContainer.querySelectorAll('.course-card');
        courseCards.forEach(courseCard => {
            // Get the credits from the course-card element
            const courseCredits = parseFloat(courseCard.querySelector('.course-credits').textContent) || 0;
            totalCredits += courseCredits;
        });
  
        // Update the term-credits element for this term
        const termCreditsElement = termDiv.querySelector('.term-credits');
        termCreditsElement.textContent = `${totalCredits.toFixed(1)} / 20.0`; // Assuming 20.0 is the maximum credits per term
    });
  }

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

async function getSchedule() {
    console.log('Saving schedule');
    try {
        const response = await axios.post('http://127.0.0.1:5000/getScheduleBack');
        console.log('Response from backend:', response.data.courseInfo);
        return response.data.courseInfo; // Return the actual response data
    } catch (error) {
        console.error('Error sending message to backend:', error);
        return null; // Return null or handle the error appropriately
    }
}

async function loadSchedule(scheduleLoaded) {
    console.log('Loading schedule');
    try {
        const response = await axios.post('http://127.0.0.1:5000/setScheduleBack', { scheduleLoaded });
        console.log('Response from backend:', response.data);
        return response.data; // Return the actual response data
    } catch (error) {
        console.error('Error sending message to backend:', error);
        return null; // Return null or handle the error appropriately
    }
}

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
    console.log('Requesting Course information on:', courseName, termNumber);
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