const plansData = {
    productivity: `
        <h6>Plans in selected category:</h6>
        <ul>
            <li>
                <strong>General Virtual Assistant</strong>
                <span>Manages complex personal and team calendars, and coordinate times for team meetings.</span>
            </li>
            <li>
                <strong>Personal Assistant</strong>
                <span>Manages your calendar both at work and outside of it.</span>
            </li>
        </ul>
    `,
    hr: `
        <h6>Plans in selected category:</h6>
        <ul>
            <li>
                <strong>HR Assistant</strong>
                <span>Handles recruitment, onboarding, and HR documentation.</span>
            </li>
            <li>
                <strong>Payroll Specialist</strong>
                <span>Manages payroll processing and compliance.</span>
            </li>
        </ul>
    `,
    sales: `
        <h6>Plans in selected category:</h6>
        <ul>
            <li>
                <strong>Sales Development Rep</strong>
                <span>Generates leads and manages CRM updates.</span>
            </li>
            <li>
                <strong>Account Executive Assistant</strong>
                <span>Supports your sales team with proposals and follow-ups.</span>
            </li>
        </ul>
    `,
    marketing: `
        <h6>Plans in selected category:</h6>
        <ul>
            <li>
                <strong>Marketing Assistant</strong>
                <span>Assists with content creation, campaign execution, and analytics.</span>
            </li>
            <li>
                <strong>Social Media Manager</strong>
                <span>Manages your brand’s social presence and engagement.</span>
            </li>
        </ul>
    `,
    customer: `
        <h6>Plans in selected category:</h6>
        <ul>
            <li>
                <strong>Customer Support Agent</strong>
                <span>Handles customer inquiries and support tickets.</span>
            </li>
            <li>
                <strong>Live Chat Assistant</strong>
                <span>Provides real-time support via chat platforms.</span>
            </li>
        </ul>
    `,
    us: `
        <h6>Plans in selected category:</h6>
        <ul>
            <li>
                <strong>US-Based Virtual Assistant</strong>
                <span>Professional support from US-based talent.</span>
            </li>
        </ul>
    `,
    healthcare: `
        <h6>Plans in selected category:</h6>
        <ul>
            <li>
                <strong>Healthcare Assistant</strong>
                <span>Helps with appointments, billing, and insurance filing.</span>
            </li>
        </ul>
    `,
    software: `
        <h6>Plans in selected category:</h6>
        <ul>
            <li>
                <strong>Web Developer</strong>
                <span>Builds and maintains your website or web app.</span>
            </li>
            <li>
                <strong>Mobile App Developer</strong>
                <span>Creates mobile solutions for your business.</span>
            </li>
        </ul>
    `,
    industry: `
        <h6>Plans in selected category:</h6>
        <ul>
            <li>
                <strong>Legal Assistant</strong>
                <span>Supports legal professionals with research and documentation.</span>
            </li>
            <li>
                <strong>Logistics Coordinator</strong>
                <span>Manages supply chain and logistics tasks.</span>
            </li>
        </ul>
    `,
    realestate: `
        <h6>Plans in selected category:</h6>
        <ul>
            <li>
                <strong>Real Estate Assistant</strong>
                <span>Manages listings, client communications, and paperwork.</span>
            </li>
        </ul>
    `
};

document.querySelectorAll('.accordion-category').forEach((cat, idx) => {
    cat.addEventListener('click', function() {
        // Remove active/open from all
        document.querySelectorAll('.accordion-category').forEach(c => c.classList.remove('active'));
        document.querySelectorAll('.accordion-panel').forEach(p => p.classList.remove('open'));
        // Add to clicked
        this.classList.add('active');
        this.nextElementSibling.classList.add('open');
        // Update plans
        const plansDiv = document.getElementById('plansContent');
        const key = this.getAttribute('data-category');
        plansDiv.innerHTML = plansData[key] || '';
    });
});