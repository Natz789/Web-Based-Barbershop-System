barbershop_system/
├── core/                              # Shared Atomic Components
│   ├── atoms/                         # Smallest units
│   │   ├── __init__.py
│   │   ├── buttons.py
│   │   ├── badges.py
│   │   ├── inputs.py
│   │   └── labels.py
│   ├── molecules/                     # Atom combinations
│   │   ├── __init__.py
│   │   ├── cards.py
│   │   ├── tables.py
│   │   └── forms.py
│   └── organisms/                     # Complex components
│       ├── __init__.py
│       ├── navigation.py
│       └── dashboard.py
│
├── security_management/               # Authentication App
│   ├── models.py                      # User, StaffProfile
│   ├── views.py                       # Uses organisms
│   ├── forms.py                       # Uses atoms/molecules
│   ├── services.py                    # Business logic
│   └── decorators.py                  # Permission decorators
│
├── booking_management/                # Booking App
│   ├── models.py                      # Booking model
│   ├── views.py                       # Uses organisms
│   ├── forms.py                       # Uses atoms/molecules
│   └── services.py                    # Business logic
│
├── payment_management/                # Payment App
│   ├── models.py                      # Payment model
│   ├── views.py                       # Uses organisms
│   └── services.py                    # Business logic
│
├── service_catalog/                   # Services App
│   ├── models.py                      # Service model
│   └── views.py                       # Uses molecules
│
└── analytics_dashboard/               # Analytics App
    ├── models.py                      # Analytics model
    └── services.py                    # Data aggregation