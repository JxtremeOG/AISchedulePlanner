// Get the delete zone element
const deleteZone = document.getElementById('delete-zone');

// Add event listeners for dragover and drop
deleteZone.addEventListener('dragover', (event) => {
  event.preventDefault(); // Prevent the default to allow dropping
  deleteZone.classList.add('drag-over'); // Add visual feedback
});

deleteZone.addEventListener('dragleave', () => {
  deleteZone.classList.remove('drag-over'); // Remove visual feedback
});

deleteZone.addEventListener('drop', (event) => {
  event.preventDefault();
  deleteZone.classList.remove('drag-over'); // Remove visual feedback
  
  const draggedItem = document.querySelector('.is-dragging'); // Get the dragged item
  
  if (draggedItem) {
    removeCourse(draggedItem.querySelector('.course-name').textContent)
    draggedItem.remove(); // Remove the item from the DOM
    console.log('Item deleted:', draggedItem);
  }
});