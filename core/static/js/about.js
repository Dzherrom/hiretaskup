// Data for the categories and plans
// Using icon names for Lucide
const plansData = {
    productivity: {
        label: "Personal Productivity",
        iconName: "users", 
        description: "Maximize your efficiency with dedicated assistants who manage personal tasks, scheduling, and executive support.",
        plans: [
            { title: "General Virtual Assistant", desc: "Manages complex personal and team calendars, and coordinate times for team meetings." },
            { title: "Personal Assistant", desc: "Manages your calendar both at work and outside of it." }
        ]
    },
    hr: {
        label: "HR, Admin and Finance",
        iconName: "briefcase",
        description: "Streamline HR and finance operations with expert assistants for payroll, onboarding, and admin tasks.",
        plans: [
            { title: "HR Assistant", desc: "Handles recruitment, onboarding, and HR documentation." },
            { title: "Payroll Specialist", desc: "Manages payroll processing and compliance." }
        ]
    },
    sales: {
        label: "Sales Development",
        iconName: "trending-up",
        description: "Boost your sales pipeline with assistants skilled in lead generation, outreach, and CRM management.",
        plans: [
            { title: "Sales Development Rep", desc: "Generates leads and manages CRM updates." },
            { title: "Account Executive", desc: "Supports your sales team with proposals and follow-ups." }
        ]
    },
    marketing: {
        label: "Marketing",
        iconName: "megaphone",
        description: "Drive marketing success with assistants who manage content creation, campaign execution, and performance analysis.",
        plans: [
            { title: "Marketing Assistant", desc: "Assists with content creation, campaign execution, and analytics." },
            { title: "Social Media Manager", desc: "Manages your brand’s social presence and engagement." }
        ]
    },
    customer: {
        label: "Customer Service",
        iconName: "headphones",
        description: "Enhance customer satisfaction with dedicated support for inquiries, complaints, and feedback.",
        plans: [
            { title: "Customer Support Agent", desc: "Handles customer inquiries and support tickets." },
            { title: "Live Chat Assistant", desc: "Provides real-time support via chat platforms." }
        ]
    },
    us: {
        label: "US-Based Talents",
        iconName: "flag",
        description: "Access top-tier US-based professionals for specialized business needs and compliance.",
        plans: [
            { title: "US-Based Virtual Assistant", desc: "Professional support from US-based talent." }
        ]
    },
    healthcare: {
        label: "Healthcare",
        iconName: "stethoscope",
        description: "Support your healthcare practice with assistants for appointment scheduling, billing, and patient follow-up.",
        plans: [
            { title: "Healthcare Assistant", desc: "Helps with appointments, billing, and insurance filing." }
        ]
    },
    software: {
        label: "Software Developers",
        iconName: "code-2",
        description: "Accelerate your tech projects with skilled software developers for web, mobile, and backend solutions.",
        plans: [
            { title: "Web Developer", desc: "Builds and maintains your website or web app." },
            { title: "Mobile App Developer", desc: "Creates mobile solutions for your business." }
        ]
    },
    industry: {
        label: "Industry-specific",
        iconName: "building-2",
        description: "Find tailored solutions for your industry, from legal to logistics and everything in between.",
        plans: [
            { title: "Legal Assistant", desc: "Supports legal professionals with research and documentation." },
            { title: "Logistics Coordinator", desc: "Manages supply chain and logistics tasks." }
        ]
    },
    realestate: {
        label: "Real Estate",
        iconName: "home",
        description: "Manage listings, client communications, and paperwork with real estate virtual assistants.",
        plans: [
            { title: "Real Estate Assistant", desc: "Manages listings, client communications, and paperwork." }
        ]
    }
};

document.addEventListener('DOMContentLoaded', () => {
    let activeCategory = 'productivity';
    
    // Initialize icons
    lucide.createIcons();

    const sidebarContainer = document.getElementById('sidebar-container');
    const plansGrid = document.getElementById('plans-grid');
    const activeIconContainer = document.getElementById('active-icon-container');
    const activeTitle = document.getElementById('active-title');
    const activeDescription = document.getElementById('active-description');
    
    // Header elements for sticky effect
    const header = document.getElementById('main-header');
    const brandText = document.getElementById('brand-text');
    const navLinks = document.getElementById('nav-links');
    const headerCta = document.getElementById('header-cta');

    // Scroll Handler
    window.addEventListener('scroll', () => {
        if (!header) return;
        if (window.scrollY > 20) {
            header.classList.remove('bg-transparent', 'py-6');
            header.classList.add('bg-white/80', 'backdrop-blur-md', 'border-b', 'border-slate-200', 'shadow-sm', 'py-4');
            
            if(brandText) {
                brandText.classList.remove('text-white');
                brandText.classList.add('text-slate-900');
            }
            
            if(navLinks) {
                navLinks.classList.remove('text-slate-200');
                navLinks.classList.add('text-slate-600');
            }
            
            if(headerCta) {
                headerCta.classList.remove('bg-white', 'text-slate-900', 'hover:bg-slate-100');
                headerCta.classList.add('bg-slate-900', 'text-white', 'hover:bg-slate-800');
            }
        } else {
            header.classList.add('bg-transparent', 'py-6');
            header.classList.remove('bg-white/80', 'backdrop-blur-md', 'border-b', 'border-slate-200', 'shadow-sm', 'py-4');
            
            if(brandText) {
                brandText.classList.add('text-white');
                brandText.classList.remove('text-slate-900');
            }
            
            if(navLinks) {
                navLinks.classList.add('text-slate-200');
                navLinks.classList.remove('text-slate-600');
            }
            
            if(headerCta) {
                headerCta.classList.add('bg-white', 'text-slate-900', 'hover:bg-slate-100');
                headerCta.classList.remove('bg-slate-900', 'text-white', 'hover:bg-slate-800');
            }
        }
    });

    // Render Sidebar
    function renderSidebar() {
        if(!sidebarContainer) return;
        sidebarContainer.innerHTML = '';
        Object.entries(plansData).forEach(([key, data]) => {
            const btn = document.createElement('button');
            const isActive = activeCategory === key;
            
            btn.className = `w-full text-left px-4 py-3 rounded-lg flex items-center gap-3 transition-all duration-200 group relative overflow-hidden ${
                isActive 
                ? 'bg-white text-blue-600 shadow-sm ring-1 ring-slate-200 active-sidebar-item' 
                : 'text-slate-600 hover:bg-slate-200/50 hover:text-slate-900'
            }`;
            
            btn.onclick = () => {
                activeCategory = key;
                renderSidebar();
                renderContent();
            };

            const indicator = isActive ? `<div class="absolute left-0 top-0 bottom-0 w-1 bg-blue-600 rounded-l-lg"></div>` : '';
            const iconClass = isActive ? 'text-blue-600' : 'text-slate-400 group-hover:text-slate-600';

            btn.innerHTML = `
                ${indicator}
                <span class="${iconClass}">
                   <i data-lucide="${data.iconName}" class="w-5 h-5"></i>
                </span>
                <span class="font-medium text-sm">${data.label}</span>
            `;
            
            sidebarContainer.appendChild(btn);
        });
        
        // Re-init icons for new elements
        if (window.lucide) lucide.createIcons();
    }

    // Render Main Content
    function renderContent() {
        if(!plansGrid) return;
        const data = plansData[activeCategory];
        
        // Update Header
        if(activeIconContainer) activeIconContainer.innerHTML = `<i data-lucide="${data.iconName}" class="w-5 h-5"></i>`;
        if(activeTitle) activeTitle.textContent = data.label;
        if(activeDescription) activeDescription.textContent = data.description;
        
        // Update Grid
        plansGrid.innerHTML = '';
        data.plans.forEach(plan => {
            const card = document.createElement('div');
            card.className = "group relative bg-slate-50 hover:bg-white rounded-xl p-6 border border-slate-200 hover:border-cyan-200 hover:shadow-lg hover:shadow-cyan-100 transition-all duration-300 cursor-pointer";
            
            card.innerHTML = `
                <div class="flex items-start gap-4">
                    <div class="mt-1 w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-400 group-hover:text-cyan-500 group-hover:border-cyan-200 transition-colors">
                        <i data-lucide="check-circle-2" class="w-5 h-5"></i>
                    </div>
                    <div>
                        <h3 class="text-lg font-bold text-slate-900 group-hover:text-blue-700 transition-colors">
                            ${plan.title}
                        </h3>
                        <p class="text-slate-500 mt-2 leading-relaxed text-sm group-hover:text-slate-600">
                            ${plan.desc}
                        </p>
                    </div>
                    <i data-lucide="arrow-right" class="w-5 h-5 text-slate-300 absolute top-6 right-6 opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-300"></i>
                </div>
            `;
            plansGrid.appendChild(card);
        });

        // Re-init icons
        if (window.lucide) lucide.createIcons();
    }

    // Initial Render
    renderSidebar();
    renderContent();
});
