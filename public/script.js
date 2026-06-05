// API Configuration
const API_URL = 'https://ai-wealth-agent.onrender.com';

// DOM Elements
const queryForm = document.getElementById('queryForm');
const queryInput = document.getElementById('queryInput');
const submitBtn = document.getElementById('submitBtn');
const errorAlert = document.getElementById('errorAlert');
const resultsSection = document.getElementById('resultsSection');
const quickTips = document.getElementById('quickTips');
const tabButtons = document.querySelectorAll('.tab-button');
const portfolioFile = document.getElementById('portfolioFile');

// Tab switching functionality
tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.getAttribute('data-tab');

        // Remove active class from all buttons and contents
        tabButtons.forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });

        // Add active class to clicked button and corresponding content
        button.classList.add('active');
        document.getElementById(tabName).classList.add('active');
    });
});

// Form submission
queryForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const query = queryInput.value.trim();
    if (!query) {
        showError('Please enter a query');
        return;
    }

    await handleQuery(query);
});

// Handle query submission
async function handleQuery(query) {
    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ Analyzing...';
    errorAlert.classList.remove('show');
    errorAlert.textContent = '';

    try {
        const formData = new FormData();

        formData.append("query", query);

        if (portfolioFile.files.length > 0) {
            formData.append(
                "file",
                portfolioFile.files[0]
            );
        }

        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
        }

        const data = await response.json();
        displayResults(data);
        resultsSection.classList.add('show');
        quickTips.style.display = 'none';

        // Reset to first tab
        tabButtons[0].click();
    } catch (err) {
        showError(
            err.message ||
            'Failed to fetch results. Make sure the backend is running on http://localhost:8000'
        );
        resultsSection.classList.remove('show');
        quickTips.style.display = 'grid';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Analyze';
    }
}

// Display results in tabs
function displayResults(data) {
    const tabMap = {
        stock_price: 'stock-text',
        portfolio_analysis: 'portfolio-text',
        sip_result: 'sip-text',
        retirement_plan: 'retirement-text',
        risk_profile: 'risk-text',
        final_response: 'advice-text',
    };

    for (const [key, elementId] of Object.entries(tabMap)) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerText = cleanResponse(data[key] || 'No data available for this section');
        }
    }
}

// Show error message
function showError(message) {
    errorAlert.textContent = message;
    errorAlert.classList.add('show');
}

function cleanResponse(text) {
    return text
        .replace(/#+/g, "")
        .replace(/\*+/g, "")
        .replace(/={2,}/g, "")
        .replace(/-{2,}/g, "");
}

// Initialize
console.log('Backend URL:', API_URL);