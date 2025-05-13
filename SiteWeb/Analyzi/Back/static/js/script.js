document.addEventListener("DOMContentLoaded", () => {
  // App switching functionality
  const equipmentBtn = document.getElementById("equipment-btn")
  const motorBtn = document.getElementById("motor-btn")
  const equipmentApp = document.getElementById("equipment-app")
  const motorApp = document.getElementById("motor-app")

  if (equipmentBtn && motorBtn) {
    equipmentBtn.addEventListener("click", () => {
      equipmentBtn.classList.add("active")
      motorBtn.classList.remove("active")
      equipmentApp.classList.add("active")
      motorApp.classList.remove("active")

      // Update URL parameter to track current app
      const url = new URL(window.location.href)
      url.searchParams.set("app", "equipment")
      window.history.replaceState({}, "", url)
    })

    motorBtn.addEventListener("click", () => {
      motorBtn.classList.add("active")
      equipmentBtn.classList.remove("active")
      motorApp.classList.add("active")
      equipmentApp.classList.remove("active")

      // Update URL parameter to track current app
      const url = new URL(window.location.href)
      url.searchParams.set("app", "motor")
      window.history.replaceState({}, "", url)
    })

    // Check URL parameters on load to set correct app
    const urlParams = new URLSearchParams(window.location.search)
    const appParam = urlParams.get("app")
    if (appParam === "motor") {
      motorBtn.click()
    } else if (appParam === "equipment") {
      equipmentBtn.click()
    }
  }

  // Equipment Lifetime Predictor functionality
  const newEquipmentPredictionBtn = document.getElementById("new-equipment-prediction")
  if (newEquipmentPredictionBtn) {
    newEquipmentPredictionBtn.addEventListener("click", () => {
      window.location.href = "/?app=equipment"
    })
  }

  // Counter animation for prediction value
  const predictionElement = document.getElementById("prediction-counter")
  if (predictionElement) {
    const predictionValue = Number.parseFloat(predictionElement.getAttribute("data-value"))

    // Set up animation variables
    let currentValue = 0
    const duration = 2000 // 2 seconds
    const steps = 60
    const increment = predictionValue / steps
    const interval = duration / steps

    // Start the counter animation
    const counter = setInterval(() => {
      currentValue += increment
      if (currentValue >= predictionValue) {
        currentValue = predictionValue
        clearInterval(counter)
      }
      predictionElement.textContent = currentValue.toFixed(2)
    }, interval)
  }

  // Motor Sound Analyzer functionality
  const audioUpload = document.getElementById("audio-upload")
  const selectFileBtn = document.getElementById("select-file-btn")
  const dropArea = document.getElementById("drop-area")
  const selectedFile = document.getElementById("selected-file")
  const fileName = document.getElementById("file-name")
  const analyzeBtn = document.getElementById("analyze-btn")
  const clearBtn = document.getElementById("clear-btn")
  const analyzeText = document.getElementById("analyze-text")
  const loadingSpinner = document.getElementById("loading-spinner")
  const analyzeAnotherBtn = document.getElementById("analyze-another-btn")

  // File selection
  if (selectFileBtn && audioUpload) {
    selectFileBtn.addEventListener("click", () => {
      audioUpload.click()
    })
  }

  if (audioUpload) {
    audioUpload.addEventListener("change", () => {
      if (audioUpload.files.length > 0) {
        showSelectedFile(audioUpload.files[0])
      }
    })
  }

  // Drag and drop functionality
  if (dropArea) {
    ;["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
      dropArea.addEventListener(eventName, preventDefaults, false)
    })

    function preventDefaults(e) {
      e.preventDefault()
      e.stopPropagation()
    }
    ;["dragenter", "dragover"].forEach((eventName) => {
      dropArea.addEventListener(eventName, highlight, false)
    })
    ;["dragleave", "drop"].forEach((eventName) => {
      dropArea.addEventListener(eventName, unhighlight, false)
    })

    function highlight() {
      dropArea.classList.add("highlight")
    }

    function unhighlight() {
      dropArea.classList.remove("highlight")
    }

    dropArea.addEventListener("drop", handleDrop, false)

    function handleDrop(e) {
      const dt = e.dataTransfer
      const files = dt.files

      if (files.length > 0) {
        audioUpload.files = files
        showSelectedFile(files[0])
      }
    }
  }

  function showSelectedFile(file) {
    if (fileName && selectedFile && dropArea && analyzeBtn) {
      fileName.textContent = file.name
      selectedFile.style.display = "block"
      dropArea.style.display = "none"
      analyzeBtn.disabled = false
    }
  }

  // Clear button functionality
  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      if (audioUpload && selectedFile && dropArea && analyzeBtn && fileName) {
        audioUpload.value = ""
        selectedFile.style.display = "none"
        dropArea.style.display = "block"
        analyzeBtn.disabled = true
        fileName.textContent = ""
      }
    })
  }

  // Form submission
  const audioForm = document.getElementById("audio-form")
  if (audioForm && analyzeText && loadingSpinner) {
    audioForm.addEventListener("submit", (event) => {
      // Prevent default submission
      event.preventDefault()

      analyzeText.style.display = "none"
      loadingSpinner.style.display = "inline-block"
      analyzeBtn.disabled = true

      // Get current URL parameters and ensure we add the app parameter
      const urlParams = new URLSearchParams(window.location.search)
      urlParams.set("app", "motor")

      // Update form action with parameters
      audioForm.action = `/analyze-motor?${urlParams.toString()}`
      audioForm.submit()
    })
  }

  // Analyze another audio button
  if (analyzeAnotherBtn) {
    analyzeAnotherBtn.addEventListener("click", () => {
      window.location.href = "/?app=motor"
    })
  }

  // Visualization tabs
  const vizTabBtns = document.querySelectorAll(".viz-tab-btn")
  if (vizTabBtns.length > 0) {
    vizTabBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        // Remove active class from all buttons and panes
        document.querySelectorAll(".viz-tab-btn").forEach((b) => b.classList.remove("active"))
        document.querySelectorAll(".viz-tab-pane").forEach((p) => p.classList.remove("active"))

        // Add active class to clicked button and corresponding pane
        btn.classList.add("active")
        const vizType = btn.getAttribute("data-viz")
        document.getElementById(`viz-${vizType}`).classList.add("active")
      })
    })
  }

  // Language selection
  window.setLanguage = (lang) => {
    console.log("Language changed to:", lang)
    // Here you would implement the actual language change logic
  }

  // Mobile menu toggle
  const mobileMenuBtn = document.querySelector(".mobile-menu-btn")
  const navLinks = document.querySelector(".nav-links")

  if (mobileMenuBtn && navLinks) {
    mobileMenuBtn.addEventListener("click", () => {
      navLinks.style.display = navLinks.style.display === "flex" ? "none" : "flex"
    })
  }

  // Add fadeIn class to all elements with animations
  const animatedElements = document.querySelectorAll(
    ".card, .results-card, .step, .condition, .machine-type, .viz-container img, .tab-btn, .viz-tab-btn",
  )
  animatedElements.forEach((el) => {
    el.classList.add("fadeIn")
  })

  // Fix for tab panes
  const tabPanes = document.querySelectorAll(".tab-pane.active, .viz-tab-pane.active")
  tabPanes.forEach((el) => {
    el.style.opacity = "1"
    el.style.transform = "translateY(0)"
  })
})
