# Blood Donation Management System

A comprehensive Django-based web application for managing blood donation operations, donor registration, blood bank inventory, and blood requests.

## Features

### Donor Management
- Donor registration and profile management
- Blood type tracking and eligibility status
- Donation history and statistics
- Search and filter functionality

### Blood Bank Management
- Blood bank registration and management
- Real-time inventory tracking
- Blood type availability monitoring
- Donation scheduling and tracking

### Blood Request System
- Hospital blood request processing
- Priority-based request management
- Request approval and fulfillment workflow
- Automated inventory updates

### Admin Interface
- Comprehensive Django admin interface
- Advanced filtering and search capabilities
- Bulk operations for efficient management
- Detailed reporting and analytics

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (default), supports PostgreSQL, MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Forms**: Django Forms with crispy-forms
- **Admin**: Django Admin Interface

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd blood-donation-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Project Structure

```
blood_donation_system/
├── blood_donation_system/     # Main project settings
├── donors/                    # Donor management app
│   ├── models.py             # Donor model
│   ├── views.py              # Donor views
│   ├── forms.py              # Donor forms
│   ├── admin.py              # Admin interface
│   └── urls.py               # URL routing
├── blood_bank/               # Blood bank management app
│   ├── models.py             # BloodBank, Inventory, Donation models
│   ├── views.py              # Blood bank views
│   ├── admin.py              # Admin interface
│   └── urls.py               # URL routing
├── requests/                 # Blood request management app
│   ├── models.py             # BloodRequest model
│   ├── views.py              # Request views
│   ├── admin.py              # Admin interface
│   └── urls.py               # URL routing
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                # Project documentation
```

## Models Overview

### Donor Model
- Personal information (name, email, phone, address)
- Blood type and eligibility status
- Donation history and statistics
- Age validation and contact information

### BloodBank Model
- Blood bank information and contact details
- Location and operational status
- Associated inventory and donations

### BloodInventory Model
- Real-time blood type availability
- Units available and reserved
- Automatic updates on donations

### Donation Model
- Donation scheduling and tracking
- Status management (scheduled, completed, cancelled)
- Automatic inventory updates

### BloodRequest Model
- Hospital request processing
- Priority and status management
- Medical information tracking
- Approval and fulfillment workflow

## Usage

### For Administrators
1. Access the admin interface at `/admin/`
2. Use the comprehensive admin panels to manage:
   - Donors and their information
   - Blood banks and inventory
   - Donations and scheduling
   - Blood requests and approvals

### For Staff
1. Register new donors through the donor registration form
2. Schedule and track donations
3. Process blood requests from hospitals
4. Monitor inventory levels

### For Donors
1. Register as a new donor
2. View donation history and eligibility
3. Schedule donation appointments

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team or create an issue in the repository.

## Future Enhancements

- Email notifications and reminders
- Mobile application
- Advanced analytics and reporting
- Integration with hospital systems
- Blood compatibility checking
- Emergency request handling
- Donor rewards and recognition system 