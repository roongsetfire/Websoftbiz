// static/js/tailwind-utilities.js
// JavaScript Utilities to replace Bootstrap components

/**
 * Modal Component
 */
class Modal {
    constructor(element) {
        this.modal = typeof element === 'string' ? document.querySelector(element) : element;
        this.isOpen = false;
        this.init();
    }

    init() {
        // Close modal when clicking backdrop
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.hide();
            }
        });

        // Close modal with Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.hide();
            }
        });
    }

    show() {
        this.modal.classList.remove('hidden');
        this.modal.classList.add('flex');
        document.body.classList.add('overflow-hidden');
        this.isOpen = true;
        
        // Animate in
        setTimeout(() => {
            this.modal.querySelector('.modal-content').classList.add('animate-fade-in');
        }, 10);
    }

    hide() {
        const content = this.modal.querySelector('.modal-content');
        content.classList.remove('animate-fade-in');
        content.classList.add('animate-fade-out');
        
        setTimeout(() => {
            this.modal.classList.add('hidden');
            this.modal.classList.remove('flex');
            document.body.classList.remove('overflow-hidden');
            content.classList.remove('animate-fade-out');
            this.isOpen = false;
        }, 300);
    }

    toggle() {
        this.isOpen ? this.hide() : this.show();
    }
}

/**
 * Dropdown Component
 */
class Dropdown {
    constructor(trigger, menu) {
        this.trigger = typeof trigger === 'string' ? document.querySelector(trigger) : trigger;
        this.menu = typeof menu === 'string' ? document.querySelector(menu) : menu;
        this.isOpen = false;
        this.init();
    }

    init() {
        this.trigger.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggle();
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.trigger.contains(e.target) && !this.menu.contains(e.target)) {
                this.hide();
            }
        });

        // Close with Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.hide();
            }
        });
    }

    show() {
        this.menu.classList.remove('hidden');
        this.menu.classList.add('animate-fade-in');
        this.isOpen = true;
    }

    hide() {
        this.menu.classList.add('hidden');
        this.menu.classList.remove('animate-fade-in');
        this.isOpen = false;
    }

    toggle() {
        this.isOpen ? this.hide() : this.show();
    }
}

/**
 * Alert/Toast Component
 */
class Toast {
    constructor(options = {}) {
        this.options = {
            message: '',
            type: 'info', // success, warning, danger, info
            duration: 5000,
            position: 'top-right',
            ...options
        };
    }

    show() {
        const toast = this.createElement();
        const container = this.getContainer();
        
        container.appendChild(toast);
        
        // Animate in
        setTimeout(() => {
            toast.classList.add('animate-slide-in-right');
        }, 10);

        // Auto remove
        if (this.options.duration > 0) {
            setTimeout(() => {
                this.remove(toast);
            }, this.options.duration);
        }

        return toast;
    }

    createElement() {
        const toast = document.createElement('div');
        toast.className = `
            relative bg-white border-l-4 rounded-r-lg shadow-lg p-4 pr-12 mb-3 max-w-sm
            ${this.getTypeClasses()}
        `;

        const icon = this.getIcon();
        
        toast.innerHTML = `
            <div class="flex items-center">
                <div class="flex-shrink-0">
                    <i class="${icon} text-lg"></i>
                </div>
                <div class="ml-3">
                    <p class="text-sm font-medium">${this.options.message}</p>
                </div>
            </div>
            <button onclick="this.parentElement.remove()" class="absolute top-3 right-3 text-gray-400 hover:text-gray-600 transition-colors duration-200">
                <i class="fas fa-times text-sm"></i>
            </button>
        `;

        return toast;
    }

    getTypeClasses() {
        const types = {
            success: 'border-green-500 bg-green-50 text-green-800',
            warning: 'border-yellow-500 bg-yellow-50 text-yellow-800',
            danger: 'border-red-500 bg-red-50 text-red-800',
            info: 'border-blue-500 bg-blue-50 text-blue-800'
        };
        return types[this.options.type] || types.info;
    }

    getIcon() {
        const icons = {
            success: 'fas fa-check-circle text-green-500',
            warning: 'fas fa-exclamation-triangle text-yellow-500',
            danger: 'fas fa-exclamation-circle text-red-500',
            info: 'fas fa-info-circle text-blue-500'
        };
        return icons[this.options.type] || icons.info;
    }

    getContainer() {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'fixed top-4 right-4 z-50';
            document.body.appendChild(container);
        }
        return container;
    }

    remove(toast) {
        toast.classList.remove('animate-slide-in-right');
        toast.classList.add('animate-slide-out-right');
        
        setTimeout(() => {
            if (toast.parentElement) {
                toast.parentElement.removeChild(toast);
            }
        }, 300);
    }

    static success(message, options = {}) {
        return new Toast({ ...options, message, type: 'success' }).show();
    }

    static warning(message, options = {}) {
        return new Toast({ ...options, message, type: 'warning' }).show();
    }

    static error(message, options = {}) {
        return new Toast({ ...options, message, type: 'danger' }).show();
    }

    static info(message, options = {}) {
        return new Toast({ ...options, message, type: 'info' }).show();
    }
}

/**
 * Accordion Component
 */
class Accordion {
    constructor(element) {
        this.accordion = typeof element === 'string' ? document.querySelector(element) : element;
        this.init();
    }

    init() {
        const headers = this.accordion.querySelectorAll('.accordion-header');
        headers.forEach(header => {
            header.addEventListener('click', () => {
                const content = header.nextElementSibling;
                const isOpen = !content.classList.contains('hidden');
                
                // Close all others (if single open behavior wanted)
                // this.closeAll();
                
                if (isOpen) {
                    this.close(content);
                } else {
                    this.open(content);
                }
            });
        });
    }

    open(content) {
        content.classList.remove('hidden');
        content.style.maxHeight = content.scrollHeight + 'px';
    }

    close(content) {
        content.style.maxHeight = '0px';
        setTimeout(() => {
            content.classList.add('hidden');
        }, 300);
    }

    closeAll() {
        const contents = this.accordion.querySelectorAll('.accordion-content');
        contents.forEach(content => this.close(content));
    }
}

/**
 * Tab Component
 */
class Tabs {
    constructor(element) {
        this.tabContainer = typeof element === 'string' ? document.querySelector(element) : element;
        this.init();
    }

    init() {
        const tabButtons = this.tabContainer.querySelectorAll('.tab-button');
        const tabContents = this.tabContainer.querySelectorAll('.tab-content');

        tabButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = button.getAttribute('data-tab');
                
                // Remove active class from all tabs and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.add('hidden'));
                
                // Add active class to clicked tab and show content
                button.classList.add('active');
                const targetContent = document.getElementById(targetId);
                if (targetContent) {
                    targetContent.classList.remove('hidden');
                    targetContent.classList.add('animate-fade-in');
                }
            });
        });
    }
}

/**
 * Form Validation
 */
class FormValidator {
    constructor(form, options = {}) {
        this.form = typeof form === 'string' ? document.querySelector(form) : form;
        this.options = {
            showErrors: true,
            validateOnInput: true,
            ...options
        };
        this.errors = {};
        this.init();
    }

    init() {
        if (this.options.validateOnInput) {
            const inputs = this.form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                input.addEventListener('input', () => {
                    this.validateField(input);
                });
                
                input.addEventListener('blur', () => {
                    this.validateField(input);
                });
            });
        }

        this.form.addEventListener('submit', (e) => {
            if (!this.validate()) {
                e.preventDefault();
            }
        });
    }

    validate() {
        this.errors = {};
        const inputs = this.form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            this.validateField(input);
        });

        if (this.options.showErrors) {
            this.displayErrors();
        }

        return Object.keys(this.errors).length === 0;
    }

    validateField(field) {
        const value = field.value.trim();
        const rules = this.getRules(field);
        const fieldName = field.name || field.id;

        // Clear previous errors for this field
        delete this.errors[fieldName];

        // Required validation
        if (rules.required && !value) {
            this.errors[fieldName] = 'ฟิลด์นี้จำเป็นต้องกรอก';
            return;
        }

        // Email validation
        if (rules.email && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                this.errors[fieldName] = 'รูปแบบอีเมลไม่ถูกต้อง';
                return;
            }
        }

        // Min length validation
        if (rules.minLength && value.length < rules.minLength) {
            this.errors[fieldName] = `ต้องมีอย่างน้อย ${rules.minLength} ตัวอักษร`;
            return;
        }

        // Pattern validation
        if (rules.pattern && value) {
            const regex = new RegExp(rules.pattern);
            if (!regex.test(value)) {
                this.errors[fieldName] = rules.patternMessage || 'รูปแบบไม่ถูกต้อง';
                return;
            }
        }

        // Clear error styling if validation passes
        this.clearFieldError(field);
    }

    getRules(field) {
        return {
            required: field.hasAttribute('required'),
            email: field.type === 'email',
            minLength: field.getAttribute('minlength'),
            pattern: field.getAttribute('pattern'),
            patternMessage: field.getAttribute('data-pattern-message')
        };
    }

    displayErrors() {
        // Clear all previous error displays
        this.form.querySelectorAll('.error-message').forEach(el => el.remove());
        this.form.querySelectorAll('.border-red-500').forEach(el => {
            el.classList.remove('border-red-500');
            el.classList.add('border-gray-300');
        });

        // Display new errors
        Object.keys(this.errors).forEach(fieldName => {
            const field = this.form.querySelector(`[name="${fieldName}"], #${fieldName}`);
            if (field) {
                this.showFieldError(field, this.errors[fieldName]);
            }
        });
    }

    showFieldError(field, message) {
        field.classList.remove('border-gray-300');
        field.classList.add('border-red-500');

        const errorElement = document.createElement('div');
        errorElement.className = 'error-message text-red-600 text-sm mt-1';
        errorElement.textContent = message;

        field.parentNode.appendChild(errorElement);
    }

    clearFieldError(field) {
        field.classList.remove('border-red-500');
        field.classList.add('border-gray-300');

        const errorElement = field.parentNode.querySelector('.error-message');
        if (errorElement) {
            errorElement.remove();
        }
    }
}

/**
 * Loading Spinner
 */
class LoadingSpinner {
    static show(target = 'body', options = {}) {
        const targetElement = typeof target === 'string' ? document.querySelector(target) : target;
        const config = {
            message: 'กำลังโหลด...',
            overlay: true,
            ...options
        };

        const spinner = document.createElement('div');
        spinner.id = 'loading-spinner';
        spinner.className = `
            ${config.overlay ? 'fixed inset-0 bg-black bg-opacity-50' : 'absolute inset-0 bg-white bg-opacity-75'}
            flex items-center justify-center z-50
        `;

        spinner.innerHTML = `
            <div class="bg-white rounded-lg p-6 flex flex-col items-center shadow-xl">
                <div class="spinner border-softbiz-blue mb-4"></div>
                <p class="text-gray-700 text-sm">${config.message}</p>
            </div>
        `;

        if (config.overlay) {
            document.body.appendChild(spinner);
        } else {
            targetElement.style.position = 'relative';
            targetElement.appendChild(spinner);
        }

        return spinner;
    }

    static hide() {
        const spinner = document.getElementById('loading-spinner');
        if (spinner) {
            spinner.remove();
        }
    }
}

/**
 * Utility Functions
 */
const TailwindUtils = {
    // Smooth scroll to element
    scrollTo(target, offset = 0) {
        const element = typeof target === 'string' ? document.querySelector(target) : target;
        if (element) {
            const targetPosition = element.offsetTop - offset;
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    },

    // Debounce function
    debounce(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    },

    // Throttle function
    throttle(func, delay) {
        let inThrottle;
        return function (...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, delay);
            }
        };
    },

    // Copy to clipboard
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            Toast.success('คัดลอกไปยังคลิปบอร์ดแล้ว');
        } catch (err) {
            Toast.error('ไม่สามารถคัดลอกได้');
        }
    },

    // Format currency
    formatCurrency(amount, currency = 'THB') {
        return new Intl.NumberFormat('th-TH', {
            style: 'currency',
            currency: currency,
            minimumFractionDigits: 2
        }).format(amount);
    },

    // Format date
    formatDate(date, options = {}) {
        const defaultOptions = {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        };
        return new Intl.DateTimeFormat('th-TH', { ...defaultOptions, ...options }).format(new Date(date));
    },

    // Check if element is in viewport
    isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    },

    // Animate element
    animate(element, animation, duration = 300) {
        return new Promise(resolve => {
            element.classList.add(animation);
            setTimeout(() => {
                element.classList.remove(animation);
                resolve();
            }, duration);
        });
    }
};

// Auto-initialize components when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Modals
    document.querySelectorAll('[data-modal-trigger]').forEach(trigger => {
        const modalId = trigger.getAttribute('data-modal-trigger');
        const modal = document.getElementById(modalId);
        if (modal) {
            const modalInstance = new Modal(modal);
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                modalInstance.show();
            });
        }
    });

    // Initialize Dropdowns
    document.querySelectorAll('[data-dropdown-trigger]').forEach(trigger => {
        const menuId = trigger.getAttribute('data-dropdown-trigger');
        const menu = document.getElementById(menuId);
        if (menu) {
            new Dropdown(trigger, menu);
        }
    });

    // Initialize Accordions
    document.querySelectorAll('.accordion').forEach(accordion => {
        new Accordion(accordion);
    });

    // Initialize Tabs
    document.querySelectorAll('.tabs').forEach(tabs => {
        new Tabs(tabs);
    });

    // Initialize Forms with validation
    document.querySelectorAll('form[data-validate]').forEach(form => {
        new FormValidator(form);
    });
});

// Add additional CSS animations
const additionalStyles = `
<style>
@keyframes fadeOut {
    from { opacity: 1; transform: translateY(0); }
    to { opacity: 0; transform: translateY(-10px); }
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(100%); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes slideOutRight {
    from { opacity: 1; transform: translateX(0); }
    to { opacity: 0; transform: translateX(100%); }
}

.animate-fade-out {
    animation: fadeOut 0.3s ease-out forwards;
}

.animate-slide-in-right {
    animation: slideInRight 0.3s ease-out forwards;
}

.animate-slide-out-right {
    animation: slideOutRight 0.3s ease-out forwards;
}
</style>
`;

// Inject additional styles
document.head.insertAdjacentHTML('beforeend', additionalStyles);

// Export components for global use
window.Modal = Modal;
window.Dropdown = Dropdown;
window.Toast = Toast;
window.Accordion = Accordion;
window.Tabs = Tabs;
window.FormValidator = FormValidator;
window.LoadingSpinner = LoadingSpinner;
window.TailwindUtils = TailwindUtils;