# Atomic Design Architecture Guide

## Overview

This barbershop system follows **Atomic Design** principles to create a scalable, maintainable, and reusable component architecture.

## Project Structure

```
barbershop_system/
├── core/                              # Shared Atomic Components
│   ├── atoms/                         # Smallest units
│   │   ├── __init__.py
│   │   ├── buttons.py                # Button components
│   │   ├── inputs.py                 # Input field components
│   │   ├── labels.py                 # Label and badge components
│   │   └── typography.py             # Text components
│   ├── molecules/                     # Atom combinations
│   │   ├── __init__.py
│   │   ├── cards.py                  # Card components
│   │   ├── forms.py                  # Form field combinations
│   │   └── tables.py                 # Table components
│   ├── organisms/                     # Complex components
│   │   ├── __init__.py
│   │   ├── navigation.py             # Navigation components
│   │   ├── header.py                 # Header components
│   │   ├── footer.py                 # Footer components
│   │   └── dashboard.py              # Dashboard components
│   └── static/
│       └── css/
│           └── atomic.css            # Component styling
│
├── security_management/               # Authentication App
│   ├── models.py                     # User, StaffProfile
│   ├── views.py                      # Uses organisms
│   └── decorators.py                 # Permission decorators
│
├── booking_management/                # Booking App
│   ├── models.py                     # Booking, Service, Customer
│   ├── views.py                      # Uses organisms
│   └── services.py                   # Business logic
│
└── transaction/                       # Payment App
    ├── models.py                     # Payment, Transaction
    └── views.py                      # Uses organisms
```

## Hierarchy Explanation

### 🔴 Atoms (The Smallest Units)

Atoms represent the smallest, most fundamental, and indivisible units of the design system.

**Examples in this system:**
- `Button` - Basic button component
- `TextInput` - Text input field
- `Label` - Form label
- `Badge` - Status badge
- `Heading` - Text heading

**Location:** `core/atoms/`

**Usage:**
```python
from core.atoms.buttons import Button
from core.atoms.inputs import TextInput
from core.atoms.labels import Label

button = Button('Submit', button_type='submit', css_class='btn-primary')
text_input = TextInput('username', placeholder='Enter username')
label = Label('Username', for_field='username', required=True)
```

### 🔗 Molecules (Combinations of Atoms)

Molecules are groups of atoms bonded together that function as a cohesive, reusable unit.

**Examples in this system:**
- `FormField` - Combines Label + Input + Help Text
- `Card` - Combines Title + Content + Footer
- `Table` - Combines Headers + Rows
- `ServiceCard` - Specialized card for services

**Location:** `core/molecules/`

**Usage:**
```python
from core.molecules.forms import FormField, BookingForm
from core.molecules.cards import ServiceCard
from core.atoms.inputs import EmailInput

# Create a form field (molecule)
email_field = FormField(
    'Email',
    EmailInput('email', placeholder='Enter email', required=True),
    required=True
)

# Create a service card (molecule)
service_card = ServiceCard(
    service_name='Haircut',
    description='Professional haircut service',
    price=25.00,
    duration=30
)
```

### 🦠 Organisms (Complex Structures)

Organisms are complex structures composed of molecules and atoms, forming distinct, functional sections.

**Examples in this system:**
- `Navigation` - Full navigation bar
- `Header` - Complete page header with navigation
- `Footer` - Full footer section
- `Dashboard` - Complete dashboard with stats and tables
- `BookingsDashboard` - Specialized dashboard for bookings

**Location:** `core/organisms/`

**Usage:**
```python
from core.organisms.header import Header
from core.organisms.footer import Footer
from core.organisms.dashboard import BookingsDashboard

# Create header organism
header = Header(
    brand_name='Barbershop System',
    nav_items=[
        {'url': '/', 'label': 'Home'},
        {'url': '/services', 'label': 'Services'},
        {'url': '/book', 'label': 'Book Now'},
    ],
    user=request.user,
    show_hero=True,
    hero_title='Welcome to Premium Barbershop'
)

# Create dashboard organism
dashboard = BookingsDashboard(
    stats_data={
        'total_bookings': 150,
        'total_revenue': 5000,
        'active_customers': 75,
    },
    bookings=bookings_list
)
```

## Component Hierarchy Visual

```
┌─────────────────────────────────────────────────────────────┐
│                      ORGANISM: Header                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              MOLECULE: Navigation                      │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐                  │  │
│  │  │ ATOM:  │  │ ATOM:  │  │ ATOM:  │                  │  │
│  │  │ Link   │  │ Link   │  │ Button │                  │  │
│  │  └────────┘  └────────┘  └────────┘                  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Benefits of This Architecture

### 1. **Reusability**
Components can be used across different parts of the application:
```python
# Same button atom used in multiple places
submit_button = Button('Submit', css_class='btn-primary')
cancel_button = Button('Cancel', css_class='btn-secondary')
```

### 2. **Consistency**
All UI elements follow the same design patterns and styling.

### 3. **Maintainability**
Changes to a component automatically propagate throughout the application:
```python
# Change button styling in one place affects all buttons
# core/atoms/buttons.py
```

### 4. **Scalability**
Easy to add new components by combining existing ones:
```python
# Create new molecule from existing atoms
class SearchForm:
    def __init__(self):
        self.input = TextInput('search')
        self.button = Button('Search', css_class='btn-primary')
```

### 5. **Testability**
Components can be tested independently:
```python
def test_button_render():
    button = Button('Test', css_class='btn-primary')
    html = button.render()
    assert 'btn btn-primary' in html
```

## Best Practices

### 1. **Keep Atoms Simple**
Atoms should do one thing and do it well:
```python
# Good - single responsibility
class Button:
    def __init__(self, text, button_type='button'):
        self.text = text
        self.button_type = button_type
```

### 2. **Build Molecules from Atoms**
Always compose molecules from existing atoms:
```python
# Good - using atoms
class FormField:
    def __init__(self, label_text, input_widget):
        self.label = Label(label_text)
        self.input = input_widget
```

### 3. **Organisms Should Be Feature-Complete**
Organisms should provide complete functionality:
```python
# Good - complete feature
class BookingsDashboard:
    def __init__(self, stats, bookings):
        self.stats = StatsDashboard(stats)
        self.table = BookingTable(bookings)
```

### 4. **Use Business Logic in Services**
Keep components focused on presentation:
```python
# Good - separation of concerns
# services.py
class BookingService:
    @staticmethod
    def create_booking(data):
        # Business logic here
        pass

# views.py
def book_view(request):
    booking = BookingService.create_booking(data)
    card = BookingCard(booking)  # Just presentation
```

## Adding New Components

### Adding a New Atom
```python
# core/atoms/icons.py
class Icon:
    def __init__(self, icon_class, size='md'):
        self.icon_class = icon_class
        self.size = size

    def render(self):
        return f'<i class="{self.icon_class} icon-{self.size}"></i>'
```

### Adding a New Molecule
```python
# core/molecules/alerts.py
from core.atoms.buttons import Button
from core.atoms.typography import Paragraph

class Alert:
    def __init__(self, message, alert_type='info', dismissible=False):
        self.message = Paragraph(message)
        self.alert_type = alert_type
        if dismissible:
            self.close_btn = Button('×', css_class='close')
```

### Adding a New Organism
```python
# core/organisms/sidebar.py
from core.molecules.cards import Card
from core.atoms.buttons import Button

class AdminSidebar:
    def __init__(self, menu_items):
        self.menu_cards = [
            Card(title=item['title'], content=item['content'])
            for item in menu_items
        ]
```

## Example: Building a Complete Page

```python
from core.organisms.header import Header
from core.organisms.footer import Footer
from core.molecules.cards import ServiceCard
from core.molecules.forms import BookingForm

def service_page(request):
    # Build page using organisms and molecules
    header = Header(
        brand_name='Barbershop',
        nav_items=nav_items,
        user=request.user
    )

    services = Service.objects.all()
    service_cards = [
        ServiceCard(
            service_name=s.name,
            description=s.description,
            price=s.price,
            duration=s.duration_minutes
        )
        for s in services
    ]

    booking_form = BookingForm(
        services=[(s.id, s.name) for s in services]
    )

    footer = Footer(brand_name='Barbershop')

    context = {
        'header': header,
        'service_cards': service_cards,
        'booking_form': booking_form,
        'footer': footer,
    }

    return render(request, 'services.html', context)
```

## Styling Components

All atomic components use the CSS classes defined in `core/static/css/atomic.css`:

```css
/* Atoms */
.btn { /* Button styling */ }
.form-control { /* Input styling */ }
.badge { /* Badge styling */ }

/* Molecules */
.card { /* Card styling */ }
.form-group { /* Form field styling */ }

/* Organisms */
.navbar { /* Navigation styling */ }
.dashboard { /* Dashboard styling */ }
```

## Conclusion

This atomic design architecture provides a solid foundation for building a scalable and maintainable barbershop management system. Each component has a clear purpose and can be composed with others to create complex interfaces while maintaining code quality and reusability.
