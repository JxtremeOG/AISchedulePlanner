const searchBar = document.getElementById('search-bar');
const resultsContainer = document.getElementById('search-results');
var courseCardList = []

// Search Code
{
  let combinedCoursesData = {}; // This will hold all the JSON data

  // Load the JSON file
  const filePath = path.join(__dirname, '../courseJsons/masterJsons.json'); // Adjust the path based on your file structure

  fs.readFile(filePath, 'utf8', (err, jsonData) => {
    if (err) {
      console.error('Error reading the JSON file:', err);
      return;
    }

    // Parse the JSON data
    combinedCoursesData = JSON.parse(jsonData);
    console.log('Data loaded successfully.');
  });

  // Event listener for the search bar
  searchBar.addEventListener('input', function (event) {
    const query = event.target.value.toLowerCase();

    // Clear previous results
    resultsContainer.innerHTML = '';

    if (query.length > 0) {
      // Filter courses based on the search query from the JSON data
      const filteredCourses = Object.values(combinedCoursesData).filter((course) =>
        course.shortName.toLowerCase().includes(query)
      );

      // Display filtered courses
      filteredCourses.forEach((course) => {
        const resultItem = document.importNode(document.getElementById('course-search-card-template').content, true);
        const searchResultItemDiv = resultItem.querySelector('.search-result-item');

        searchResultItemDiv.querySelector('.course-name').textContent = course.shortName;
        searchResultItemDiv.querySelector('.course-credits').textContent = `${course.courseCredits} credits`;


        resultItem.addEventListener('dragstart', (event) => handleDragStart(event, course));

        searchResultItemDiv.addEventListener('click', async () => {
          // You would retrieve course data from the DOM or elsewhere
          var courseDetails = await requestCourseDetails(course.shortName);
          var courseDetailStatus = await getCourseStatus(course.shortName);
          courseDetails = courseDetails.courseInfo
          const dialogDiv = document.querySelector('.dialog-content');
          dialogDiv.querySelector('.course-name').textContent = courseDetails.fullName;
          dialogDiv.querySelector('.short-name').textContent = courseDetails.shortName;
          dialogDiv.querySelector('.course-desc').textContent = "Description: " + courseDetails.courseDesc;
          dialogDiv.querySelector('.course-prereqs').textContent = "Prerequisites: " + courseDetails.prereqs;
          dialogDiv.querySelector('.course-coreqs').textContent = "Corequisites: " + courseDetails.coreqs;
          dialogDiv.querySelector('.course-offered').textContent = "Offered Terms: " + courseDetails.offered;
          changeStatusIcon(courseDetailStatus, dialogDiv.querySelector('.course-status'));

          const courseData = {
              shortName: searchResultItemDiv.querySelector('.course-name').textContent,
              credits: searchResultItemDiv.querySelector('.course-credits').textContent,
              // You can add more properties if needed
          };
  
          // Send the course data to the main process to open a new window
          document.querySelector('.course-dialog').showModal()
          // ipcRenderer.send('open-course-window', courseData);
      });

        searchResultItemDiv.addEventListener("dragstart", () => {
            if (searchResultItemDiv.classList.contains('search-result-item')){
                onCourseFirstDrag(searchResultItemDiv, course)
            }
            searchResultItemDiv.classList.add("is-dragging");
        });

        searchResultItemDiv.addEventListener("dragend", async () => {
          const parentZone = searchResultItemDiv.closest('.term-div');

          if (parentZone) {
              var courseStatus = await requestCourseInformation(course.shortName, parentZone.id)
              const iconElement = searchResultItemDiv.querySelector('.status-icon');
              changeStatusIcon(courseStatus, iconElement)
          }
          updateCourseStatus();
          updateTermCredits();

          searchResultItemDiv.classList.remove("is-dragging");
        });

        resultsContainer.appendChild(searchResultItemDiv);
      });
    }
  });

  function changeStatusIcon(courseStatus, iconElement) {
    courseStatus = courseStatus.validity

    // Update the icon and status
    if (courseStatus == true) {
      iconElement.textContent = "✔"; // Checkmark icon
      iconElement.classList.remove("warning"); // Apply warning styling
      iconElement.classList.add("checkmark"); // Apply checkmark styling
    } else if (courseStatus == false) {
      iconElement.textContent = "⚠"; // Warning icon
      iconElement.classList.remove("checkmark"); // Apply checkmark styling
      iconElement.classList.add("warning"); // Apply warning styling
    }
  }
  

  // Function to handle the drag start
  function handleDragStart(event, course) {
    // Store the course object in the data transfer for later use in drop
    event.dataTransfer.setData('application/json', JSON.stringify(course));
  }

  async function updateCourseStatus() {
    for (const courseElement of courseCardList) {
      var shortName = courseElement.querySelector('.course-name').textContent;
      var courseStatus = await getCourseStatus(shortName)
      const iconElement = courseElement.querySelector('.status-icon');
      changeStatusIcon(courseStatus, iconElement)
    }
  }

  function onCourseFirstDrag(searchResultItemDiv) {
    courseCardList.push(searchResultItemDiv)
    searchResultItemDiv.classList.remove("search-result-item");
    searchResultItemDiv.classList.add("course-card");

    const statusIcon = document.createElement('i');
    statusIcon.classList.add('status-icon');

    statusIcon.textContent = "✔"; // Checkmark icon
    statusIcon.classList.add("checkmark"); // Apply checkmark styling

    // Append the status icon at the correct place in the course card
    searchResultItemDiv.appendChild(statusIcon);  // Append it inside the course-card
  }
}

// Function to calculate and update term credits
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