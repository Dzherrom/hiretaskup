const plansData = {
    productivity: [
        { title: "General Virtual Assistant", desc: "Manages complex personal and team calendars, and coordinate times for team meetings." },
        { title: "Personal Assistant", desc: "Manages your calendar both at work and outside of it." }
    ],
    hr: [
        { title: "HR Assistant", desc: "Handles recruitment, onboarding, and HR documentation." },
        { title: "Payroll Specialist", desc: "Manages payroll processing and compliance." }
    ],
    sales: [
        { title: "Sales Development Rep", desc: "Generates leads and manages CRM updates." },
        { title: "Account Executive Assistant", desc: "Supports your sales team with proposals and follow-ups." }
    ],
    marketing: [
        { title: "Marketing Assistant", desc: "Assists with content creation, campaign execution, and analytics." },
        { title: "Social Media Manager", desc: "Manages your brand’s social presence and engagement." }
    ],
    customer: [
        { title: "Customer Support Agent", desc: "Handles customer inquiries and support tickets." },
        { title: "Live Chat Assistant", desc: "Provides real-time support via chat platforms." }
    ],
    us: [
        { title: "US-Based Virtual Assistant", desc: "Professional support from US-based talent." }
    ],
    healthcare: [
        { title: "Healthcare Assistant", desc: "Helps with appointments, billing, and insurance filing." }
    ],
    software: [
        { title: "Web Developer", desc: "Builds and maintains your website or web app." },
        { title: "Mobile App Developer", desc: "Creates mobile solutions for your business." }
    ],
    industry: [
        { title: "Legal Assistant", desc: "Supports legal professionals with research and documentation." },
        { title: "Logistics Coordinator", desc: "Manages supply chain and logistics tasks." }
    ],
    realestate: [
        { title: "Real Estate Assistant", desc: "Manages listings, client communications, and paperwork." }
    ]
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
        const data = plansData[key];

        if (data) {
            let html = '<h6>Plans in selected category:</h6><ul>';
            data.forEach(plan => {
                // Generar nombre de imagen basado en el título (slugify: "General Virtual Assistant" -> "general-virtual-assistant.png")
                // Se asume que la extensión es .png y se reemplazan espacios por guiones.
                const imgName = plan.title.toLowerCase().trim().replace(/\s+/g, '-') + '.png';
                // Asumimos ruta /static/img/ para las imágenes
                const imgSrc = '/static/img/' + imgName;

                html += `
                    <li>
                        <img src="${imgSrc}" alt="${plan.title}" class="about-plans-icon">
                        <div>
                            <strong>${plan.title}</strong>
                            <span>${plan.desc}</span>
                        </div>
                    </li>
                `;
            });
            html += '</ul>';
            plansDiv.innerHTML = html;
        } else {
            plansDiv.innerHTML = '';
        }
    });
});