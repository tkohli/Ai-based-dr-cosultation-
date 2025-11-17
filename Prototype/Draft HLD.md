# High-Level Design: Integrated AI Healthcare Platform
## AI Consultation + Medicine E-Commerce + Lab Testing

---

## Executive Summary

This document presents the technical architecture for a comprehensive AI-powered healthcare platform that integrates three core services: **AI-based medical consultations, medicine e-commerce, and lab test ordering**. The platform eliminates doctor involvement entirely, relying on AI to generate prescriptions that seamlessly flow into the medicine ordering system, while also enabling direct lab test bookings with partner laboratories.

**Core Value Proposition**: A one-stop healthcare solution where patients receive AI consultations, order prescribed medicines instantly from an integrated pharmacy, and book lab tests - all within a single platform with unified user experience and data flow.

**Target Market**: Indian consumers (urban and semi-urban) seeking convenient, affordable healthcare services with fast medicine delivery and reliable lab testing facilities.

**Key Metrics**:
- **Consultation Time**: 3-5 minutes from start to prescription
- **Medicine Delivery**: 30 minutes to 2 hours (based on location)
- **Lab Booking**: Instant confirmation, sample collection within 24 hours
- **Target Scale**: 10,000 daily consultations, 15,000 medicine orders, 3,000 lab bookings

---

## Strategic Context

### Market Opportunity

**Problem Space**:
1. **Fragmented Healthcare Journey**: Patients visit multiple platforms for consultation, medicine purchase, and lab tests
2. **High Medicine Costs**: Traditional pharmacies have higher margins and limited inventory visibility
3. **Lab Test Complexity**: Booking lab tests requires phone calls, unclear pricing, and scheduling hassles
4. **Time Consumption**: Entire healthcare journey from symptom to treatment takes hours or days

**Our Solution**:
A vertically integrated platform providing end-to-end healthcare services:
- **AI Consultation** → Instant diagnosis and prescription
- **Smart Pharmacy** → One-click medicine ordering from prescription
- **Lab Network** → Seamless test booking with transparent pricing
- **Health Records** → Unified digital health history

### Business Model

**Revenue Streams**:
1. **Consultation Fees**: ₹49-99 per AI consultation
2. **Medicine Sales**: 15-25% margin on medicines (competitive with online pharmacies)
3. **Lab Commission**: 10-20% commission on lab test bookings
4. **Subscription Plans**: ₹499/month for unlimited consultations + medicine discounts
5. **Premium Features**: Health monitoring, report analysis, medicine subscriptions

**Unit Economics** (at scale):
- Average Order Value: ₹450 (₹50 consultation + ₹300 medicines + ₹100 lab tests)
- Blended Margin: 40% across all services
- Customer Acquisition Cost: ₹200
- Lifetime Value: ₹2,500 (assuming 6 consultations/year for 2 years)

---

## System Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            PATIENT WEB/MOBILE APP                            │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐         │
│  │  AI Consultation │  │   Medicine Store  │  │   Lab Booking    │         │
│  │     Module       │  │     Module        │  │     Module       │         │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘         │
└────────────────┬────────────────┬─────────────────┬────────────────────────┘
                 │                │                 │
                 ▼                ▼                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          API GATEWAY (AWS API Gateway)                       │
│                  Authentication | Rate Limiting | Routing                    │
└────────────────┬────────────────┬─────────────────┬────────────────────────┘
                 │                │                 │
      ┌──────────▼─────┐  ┌──────▼────────┐  ┌────▼──────────┐
      │  Consultation  │  │   E-Commerce  │  │  Lab Booking  │
      │    Service     │  │    Service    │  │    Service    │
      │  (AI Engine)   │  │  (Inventory)  │  │  (Partners)   │
      └────────┬───────┘  └───────┬───────┘  └───────┬───────┘
               │                  │                  │
               ▼                  ▼                  ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          SHARED SERVICES LAYER                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   Patient   │  │   Payment   │  │   Order     │  │ Notification│   │
│  │   Service   │  │   Service   │  │ Management  │  │   Service   │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
               │                  │                  │
               ▼                  ▼                  ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                           DATA & STORAGE LAYER                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ PostgreSQL  │  │  MongoDB    │  │   Redis     │  │   AWS S3    │   │
│  │ (Relational)│  │ (Documents) │  │   (Cache)   │  │   (Files)   │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
               │                  │                  │
               ▼                  ▼                  ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL INTEGRATIONS                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   OpenAI    │  │  Razorpay   │  │   Lab API   │  │  Logistics  │   │
│  │     API     │  │  (Payment)  │  │  Partners   │  │  Partners   │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

### Architecture Principles

1. **Unified Patient Experience**: Single login, seamless navigation between consultation, pharmacy, and lab services
2. **Data Integration**: Consultation history informs medicine recommendations and lab test suggestions
3. **Microservices with Shared Services**: Core services (Consultation, E-commerce, Lab) are independent but share common utilities
4. **Event-Driven Architecture**: Services communicate via events for loose coupling
5. **API-First Design**: All functionality exposed via REST/GraphQL APIs
6. **Multi-Tenant Ready**: Architecture supports white-label deployments for partners

---

## Core Service Modules

### Module 1: AI Consultation Service

**Purpose**: Conduct AI-powered medical consultations and generate prescriptions

**Key Features**:
- Conversational AI interface (text + voice-to-text)
- Multi-language support (Hindi, English, regional languages)
- Symptom analysis and prescription generation
- Medical knowledge base integration
- Safety validation and emergency detection
- Consultation history and health records

**Technical Components**:

```typescript
// Consultation Flow
interface ConsultationService {
  // Core Operations
  startConsultation(patientId: string, language: string): Consultation;
  processMessage(consultationId: string, message: string): AIResponse;
  generatePrescription(consultationId: string): Prescription;
  completeConsultation(consultationId: string): ConsultationSummary;
  
  // AI Integration
  callOpenAI(prompt: string, context: ConversationContext): string;
  validatePrescription(prescription: Prescription): ValidationResult;
  detectEmergency(symptoms: string[]): boolean;
  
  // Knowledge Base
  getMedicineInfo(medicineName: string): MedicineDetails;
  getProtocol(condition: string): TreatmentProtocol;
  checkDrugInteractions(medicines: Medicine[]): InteractionWarnings;
}

// Data Models
interface Consultation {
  id: string;
  patientId: string;
  status: 'ACTIVE' | 'COMPLETED' | 'ABANDONED';
  language: string;
  chiefComplaint: string;
  messages: Message[];
  extractedData: {
    symptoms: string[];
    duration: string;
    severity: string;
    allergies: string[];
    currentMedications: string[];
  };
  prescription?: Prescription;
  createdAt: Date;
  completedAt?: Date;
}

interface Prescription {
  id: string;
  consultationId: string;
  diagnosis: string;
  medicines: PrescribedMedicine[];
  lifestyleAdvice: string[];
  redFlags: string[];
  followUpDays: number;
  validityDays: number; // Prescription validity
  eRxNumber: string; // Electronic prescription number
}

interface PrescribedMedicine {
  medicineId: string;
  medicineName: string;
  dosage: string;
  frequency: string;
  duration: string;
  quantity: number; // Number of units to purchase
  instructions: string;
}
```

**API Endpoints**:

```
POST   /api/v1/consultations/start
POST   /api/v1/consultations/:id/messages
GET    /api/v1/consultations/:id
POST   /api/v1/consultations/:id/complete
GET    /api/v1/consultations/:id/prescription
```

**AI Safety Mechanisms**:
1. **Emergency Detection**: Redirects critical symptoms to emergency services
2. **Controlled Substances**: Blocks opioids, benzos, and high-risk medications
3. **Age Restrictions**: No prescriptions for children under 12 without guardian
4. **Confidence Threshold**: Manual review fallback for low-confidence diagnoses
5. **Drug Interactions**: Validates against patient's current medications
6. **Allergy Check**: Cross-references with patient's allergy history

---

### Module 2: Medicine E-Commerce Service

**Purpose**: Online pharmacy for medicine ordering with prescription validation

**Key Features**:
- Medicine catalog with search and filters
- Prescription-to-cart conversion (one-click from consultation)
- Generic medicine substitution suggestions
- Inventory management across multiple warehouses
- Order tracking and delivery management
- Medicine reminders and auto-refill

**Technical Components**:

```typescript
interface ECommerceService {
  // Catalog Management
  searchMedicines(query: string, filters: SearchFilters): Medicine[];
  getMedicineDetails(medicineId: string): MedicineDetails;
  getAlternatives(medicineId: string): Medicine[]; // Generic alternatives
  checkAvailability(medicineId: string, pincode: string): InventoryStatus;
  
  // Cart & Orders
  addToCart(patientId: string, items: CartItem[]): Cart;
  createOrderFromPrescription(prescriptionId: string): Order;
  validatePrescription(prescriptionId: string, items: OrderItem[]): boolean;
  placeOrder(orderId: string, deliveryAddress: Address): OrderConfirmation;
  trackOrder(orderId: string): OrderStatus;
  
  // Inventory Management
  getInventory(warehouseId: string): InventoryItem[];
  updateStock(medicineId: string, quantity: number): void;
  allocateInventory(orderId: string): AllocationResult;
  
  // Pricing & Discounts
  calculatePrice(items: CartItem[]): PriceBreakdown;
  applyDiscount(orderId: string, couponCode: string): DiscountResult;
}

// Data Models
interface Medicine {
  id: string;
  name: string;
  genericName: string;
  manufacturer: string;
  category: string;
  form: 'Tablet' | 'Capsule' | 'Syrup' | 'Injection' | 'Cream' | 'Drops';
  strength: string;
  packSize: string; // "10 tablets", "100ml bottle"
  mrp: number;
  sellingPrice: number;
  discount: number;
  prescriptionRequired: boolean;
  schedule: 'H' | 'H1' | 'X' | 'OTC'; // Drug scheduling
  images: string[];
  description: string;
  composition: string;
  uses: string[];
  sideEffects: string[];
  contraindications: string[];
}

interface Order {
  id: string;
  orderNumber: string;
  patientId: string;
  prescriptionId?: string;
  items: OrderItem[];
  pricing: {
    subtotal: number;
    medicineDiscount: number;
    deliveryCharge: number;
    tax: number;
    total: number;
  };
  deliveryAddress: Address;
  paymentMethod: string;
  paymentStatus: 'PENDING' | 'PAID' | 'FAILED';
  orderStatus: 'PLACED' | 'CONFIRMED' | 'PACKED' | 'SHIPPED' | 'DELIVERED' | 'CANCELLED';
  warehouseId: string;
  deliveryPartnerId?: string;
  trackingUrl?: string;
  estimatedDelivery: Date;
  createdAt: Date;
}

interface InventoryItem {
  medicineId: string;
  warehouseId: string;
  quantity: number;
  batchNumber: string;
  expiryDate: Date;
  reorderLevel: number;
  lastRestocked: Date;
}
```

**API Endpoints**:

```
// Medicine Catalog
GET    /api/v1/medicines/search?q={query}&category={category}
GET    /api/v1/medicines/:id
GET    /api/v1/medicines/:id/alternatives
POST   /api/v1/medicines/check-availability

// Cart & Orders
POST   /api/v1/cart/add
GET    /api/v1/cart
POST   /api/v1/orders/from-prescription/:prescriptionId
POST   /api/v1/orders
GET    /api/v1/orders/:id
GET    /api/v1/orders/:id/track

// Inventory (Internal)
GET    /api/v1/inventory/warehouse/:warehouseId
PUT    /api/v1/inventory/:medicineId/stock
```

**Smart Features**:

1. **Prescription-to-Cart Intelligence**:
```typescript
async function createOrderFromPrescription(prescriptionId: string) {
  const prescription = await getPrescription(prescriptionId);
  const cart = { items: [] };
  
  for (const medicine of prescription.medicines) {
    // Find exact medicine or generic alternative
    const availableMedicine = await findAvailableMedicine(
      medicine.medicineName,
      medicine.quantity,
      patient.pincode
    );
    
    if (!availableMedicine) {
      // Suggest alternatives
      const alternatives = await findAlternatives(medicine.medicineName);
      cart.items.push({
        prescribedMedicine: medicine,
        alternatives: alternatives,
        status: 'NEEDS_SELECTION'
      });
    } else {
      cart.items.push({
        medicineId: availableMedicine.id,
        quantity: medicine.quantity,
        status: 'AVAILABLE'
      });
    }
  }
  
  return cart;
}
```

2. **Generic Substitution Engine**:
```typescript
function suggestGenericAlternatives(brandMedicine: Medicine): Medicine[] {
  // Find medicines with same composition at lower price
  return medicines.filter(m => 
    m.composition === brandMedicine.composition &&
    m.sellingPrice < brandMedicine.sellingPrice &&
    m.id !== brandMedicine.id
  ).sort((a, b) => a.sellingPrice - b.sellingPrice);
}
```

3. **Intelligent Inventory Allocation**:
```typescript
async function allocateInventory(order: Order): Promise<AllocationResult> {
  // Find nearest warehouse with all items in stock
  const warehouses = await getWarehouses(order.deliveryAddress.pincode);
  
  for (const warehouse of warehouses) {
    const availability = await checkWarehouseInventory(
      warehouse.id,
      order.items
    );
    
    if (availability.allItemsAvailable) {
      return {
        warehouseId: warehouse.id,
        estimatedDeliveryTime: calculateDeliveryTime(
          warehouse.location,
          order.deliveryAddress
        ),
        items: availability.items
      };
    }
  }
  
  // Split order across multiple warehouses if needed
  return await splitOrderAllocation(order);
}
```

**Warehouse Management**:
- Multiple warehouse support (Delhi, Mumbai, Bangalore, etc.)
- Real-time inventory tracking
- Expiry date management (FIFO/FEFO)
- Low stock alerts and auto-reordering
- Batch tracking for quality control

---

### Module 3: Lab Testing Service

**Purpose**: Lab test booking with partner laboratories

**Key Features**:
- Lab test catalog with descriptions and pricing
- Partner lab network management
- Home sample collection scheduling
- Test report upload and management
- AI-powered report analysis
- Test recommendations based on consultation

**Technical Components**:

```typescript
interface LabService {
  // Test Catalog
  searchTests(query: string, category: string): LabTest[];
  getTestDetails(testId: string): LabTestDetails;
  getTestPackages(): LabPackage[]; // Popular test bundles
  checkLabAvailability(testId: string, pincode: string): LabPartner[];
  
  // Booking
  createBooking(patientId: string, tests: string[], labId: string): Booking;
  scheduleCollection(bookingId: string, slot: TimeSlot): boolean;
  cancelBooking(bookingId: string): boolean;
  rescheduleBooking(bookingId: string, newSlot: TimeSlot): boolean;
  
  // Reports
  uploadReport(bookingId: string, reportFile: File): Report;
  getReports(patientId: string): Report[];
  analyzeReport(reportId: string): ReportAnalysis; // AI analysis
  
  // Partner Management
  getLabPartners(pincode: string): LabPartner[];
  syncLabInventory(labId: string): void;
  updateLabPricing(labId: string, pricing: LabPricing[]): void;
}

// Data Models
interface LabTest {
  id: string;
  name: string;
  description: string;
  category: string; // "Blood", "Urine", "Imaging", "Biopsy"
  parameters: string[]; // Individual tests included
  preparation: string; // "Fasting required", "No special preparation"
  sampleType: string; // "Blood", "Urine", "Stool"
  reportTime: string; // "6 hours", "24 hours", "3 days"
  price: number;
  discountedPrice?: number;
  homeCollectionAvailable: boolean;
  homeCollectionCharge: number;
}

interface LabPartner {
  id: string;
  name: string;
  accreditation: string[]; // "NABL", "CAP", "ISO"
  rating: number;
  reviewCount: number;
  servicedPincodes: string[];
  availableTests: string[]; // test IDs
  pricing: LabPricing[];
  homeCollectionSlots: TimeSlot[];
  labLocations: LabLocation[];
}

interface Booking {
  id: string;
  bookingNumber: string;
  patientId: string;
  consultationId?: string; // If recommended by AI
  labPartnerId: string;
  tests: BookedTest[];
  collectionType: 'HOME' | 'LAB_VISIT';
  collectionAddress?: Address;
  scheduledSlot?: TimeSlot;
  pricing: {
    testCharges: number;
    homeCollectionCharge: number;
    discount: number;
    total: number;
  };
  paymentStatus: 'PENDING' | 'PAID' | 'REFUNDED';
  bookingStatus: 'SCHEDULED' | 'SAMPLE_COLLECTED' | 'PROCESSING' | 'COMPLETED' | 'CANCELLED';
  reportId?: string;
  createdAt: Date;
}

interface Report {
  id: string;
  bookingId: string;
  patientId: string;
  testResults: TestResult[];
  uploadedAt: Date;
  fileUrl: string;
  aiAnalysis?: {
    summary: string;
    abnormalFindings: string[];
    recommendations: string[];
    severity: 'NORMAL' | 'ATTENTION_NEEDED' | 'URGENT';
  };
}

interface TestResult {
  parameterName: string;
  value: string;
  unit: string;
  referenceRange: string;
  status: 'NORMAL' | 'HIGH' | 'LOW' | 'CRITICAL';
}
```

**API Endpoints**:

```
// Test Catalog
GET    /api/v1/lab/tests/search?q={query}&category={category}
GET    /api/v1/lab/tests/:id
GET    /api/v1/lab/packages
GET    /api/v1/lab/partners?pincode={pincode}

// Bookings
POST   /api/v1/lab/bookings
GET    /api/v1/lab/bookings/:id
PUT    /api/v1/lab/bookings/:id/schedule
DELETE /api/v1/lab/bookings/:id/cancel

// Reports
POST   /api/v1/lab/reports/upload
GET    /api/v1/lab/reports?patientId={patientId}
GET    /api/v1/lab/reports/:id
GET    /api/v1/lab/reports/:id/analysis
```

**Integration with Lab Partners**:

```typescript
// Lab Partner API Integration
interface LabPartnerAPI {
  // Booking Flow
  checkAvailability(testIds: string[], pincode: string): AvailabilityResponse;
  createBooking(booking: BookingRequest): BookingConfirmation;
  getAvailableSlots(pincode: string, date: Date): TimeSlot[];
  
  // Sample Collection
  confirmCollection(bookingId: string): void;
  updateStatus(bookingId: string, status: string): void;
  
  // Reports
  getReportStatus(bookingId: string): ReportStatus;
  downloadReport(bookingId: string): File;
  
  // Webhook for status updates
  onStatusUpdate(callback: (booking: Booking) => void): void;
}

// Example: Thyrocare Integration
class ThyrocareAdapter implements LabPartnerAPI {
  private apiKey: string;
  private baseUrl: string;
  
  async createBooking(booking: BookingRequest): Promise<BookingConfirmation> {
    const response = await axios.post(`${this.baseUrl}/api/ORDER/createOrder`, {
      API_KEY: this.apiKey,
      PRODUCT: booking.tests.map(t => t.code).join(','),
      MOBILE: booking.patient.mobile,
      ADDRESS: booking.address,
      PINCODE: booking.pincode,
      DATE: booking.preferredDate,
      TIME: booking.preferredSlot
    });
    
    return {
      partnerBookingId: response.data.order_id,
      status: 'CONFIRMED',
      collectionSlot: response.data.scheduled_time
    };
  }
}
```

**Smart Lab Recommendations**:

```typescript
// AI suggests relevant tests based on consultation
async function recommendLabTests(consultation: Consultation): Promise<LabTest[]> {
  const symptoms = consultation.extractedData.symptoms;
  const diagnosis = consultation.prescription?.diagnosis;
  
  const prompt = `
    Based on these symptoms: ${symptoms.join(', ')}
    And diagnosis: ${diagnosis}
    
    Recommend relevant lab tests that would help confirm diagnosis or monitor condition.
    Return as JSON array with test names.
  `;
  
  const aiResponse = await openai.chat.completions.create({
    model: "gpt-4",
    messages: [{ role: "user", content: prompt }],
    response_format: { type: "json_object" }
  });
  
  const recommendedTestNames = JSON.parse(aiResponse.choices[0].message.content).tests;
  
  // Match with our test catalog
  return await getTestsByNames(recommendedTestNames);
}
```

---

## Shared Services Layer

### Patient Service

**Purpose**: Centralized patient data management

```typescript
interface PatientService {
  // Profile Management
  createPatient(data: PatientRegistration): Patient;
  getPatient(patientId: string): Patient;
  updateProfile(patientId: string, updates: Partial<Patient>): Patient;
  
  // Health Records
  getHealthHistory(patientId: string): HealthHistory;
  addMedicalHistory(patientId: string, history: MedicalHistory): void;
  getConsultations(patientId: string): Consultation[];
  getPrescriptions(patientId: string): Prescription[];
  getOrders(patientId: string): Order[];
  getLabReports(patientId: string): Report[];
  
  // Address Management
  addAddress(patientId: string, address: Address): Address;
  getAddresses(patientId: string): Address[];
  setDefaultAddress(patientId: string, addressId: string): void;
}

interface Patient {
  id: string;
  mobile: string;
  email?: string;
  name: string;
  dateOfBirth: Date;
  gender: 'MALE' | 'FEMALE' | 'OTHER';
  bloodGroup?: string;
  emergencyContact?: {
    name: string;
    mobile: string;
    relation: string;
  };
  medicalHistory: {
    allergies: string[];
    chronicConditions: string[];
    currentMedications: string[];
    pastSurgeries: string[];
    familyHistory: string[];
  };
  addresses: Address[];
  createdAt: Date;
}
```

### Payment Service

**Purpose**: Unified payment processing for all services

```typescript
interface PaymentService {
  // Payment Processing
  createPaymentIntent(amount: number, orderId: string, type: PaymentType): PaymentIntent;
  processPayment(paymentId: string, method: PaymentMethod): PaymentResult;
  refundPayment(paymentId: string, amount: number): RefundResult;
  
  // Wallet & Credits
  getWalletBalance(patientId: string): number;
  addCredits(patientId: string, amount: number): void;
  deductCredits(patientId: string, amount: number): void;
  
  // Subscription
  createSubscription(patientId: string, plan: SubscriptionPlan): Subscription;
  cancelSubscription(subscriptionId: string): void;
}

enum PaymentType {
  CONSULTATION = 'CONSULTATION',
  MEDICINE_ORDER = 'MEDICINE_ORDER',
  LAB_BOOKING = 'LAB_BOOKING',
  SUBSCRIPTION = 'SUBSCRIPTION'
}

interface PaymentIntent {
  id: string;
  orderId: string;
  amount: number;
  currency: 'INR';
  type: PaymentType;
  razorpayOrderId: string;
  status: 'CREATED' | 'PROCESSING' | 'SUCCESS' | 'FAILED';
}
```

### Order Management Service

**Purpose**: Unified order tracking across services

```typescript
interface OrderManagementService {
  // Order Tracking
  getOrder(orderId: string, type: OrderType): Order | Booking;
  getOrderHistory(patientId: string): OrderHistory;
  updateOrderStatus(orderId: string, status: string): void;
  
  // Logistics Integration
  assignDeliveryPartner(orderId: string): DeliveryPartner;
  trackShipment(orderId: string): ShipmentStatus;
  
  // Returns & Cancellations
  cancelOrder(orderId: string, reason: string): CancellationResult;
  initiateReturn(orderId: string, items: string[]): ReturnRequest;
}

enum OrderType {
  MEDICINE = 'MEDICINE',
  LAB = 'LAB'
}
```

### Notification Service

**Purpose**: Multi-channel notifications

```typescript
interface NotificationService {
  // Send Notifications
  sendSMS(mobile: string, message: string): void;
  sendEmail(email: string, subject: string, body: string): void;
  sendPush(patientId: string, notification: PushNotification): void;
  sendWhatsApp(mobile: string, template: string, params: any): void;
  
  // Notification Templates
  consultationComplete(patientId: string, prescriptionId: string): void;
  orderConfirmed(patientId: string, orderId: string): void;
  orderShipped(patientId: string, orderId: string, trackingUrl: string): void;
  labBookingConfirmed(patientId: string, bookingId: string): void;
  reportReady(patientId: string, reportId: string): void;
  medicineReminder(patientId: string, medicine: string, time: string): void;
}
```

---

## Database Design

### PostgreSQL Schema (Relational Data)

**Patients Table**:
```sql
CREATE TABLE patients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  mobile VARCHAR(15) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE,
  name VARCHAR(100) NOT NULL,
  date_of_birth DATE,
  gender VARCHAR(20),
  blood_group VARCHAR(5),
  emergency_contact JSONB,
  medical_history JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_mobile (mobile),
  INDEX idx_email (email)
);
```

**Consultations Table**:
```sql
CREATE TABLE consultations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID REFERENCES patients(id),
  status VARCHAR(50) NOT NULL,
  language VARCHAR(10) DEFAULT 'en',
  chief_complaint TEXT,
  extracted_data JSONB,
  prescription_id UUID,
  started_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  
  INDEX idx_patient (patient_id),
  INDEX idx_status (status),
  INDEX idx_created (started_at DESC)
);
```

**Prescriptions Table**:
```sql
CREATE TABLE prescriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  consultation_id UUID REFERENCES consultations(id),
  erx_number VARCHAR(50) UNIQUE NOT NULL,
  diagnosis TEXT NOT NULL,
  medicines JSONB NOT NULL,
  lifestyle_advice TEXT[],
  red_flags TEXT[],
  validity_days INTEGER DEFAULT 30,
  confidence_level VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_consultation (consultation_id),
  INDEX idx_erx (erx_number)
);
```

**Medicines Table**:
```sql
CREATE TABLE medicines (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(200) NOT NULL,
  generic_name VARCHAR(200),
  manufacturer VARCHAR(200),
  category VARCHAR(100),
  form VARCHAR(50),
  strength VARCHAR(50),
  pack_size VARCHAR(50),
  mrp DECIMAL(10, 2),
  selling_price DECIMAL(10, 2),
  discount DECIMAL(5, 2),
  prescription_required BOOLEAN DEFAULT TRUE,
  schedule VARCHAR(5),
  composition TEXT,
  uses TEXT[],
  side_effects TEXT[],
  images TEXT[],
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_name (name),
  INDEX idx_generic (generic_name),
  INDEX idx_category (category),
  INDEX idx_price (selling_price)
);
```

**Inventory Table**:
```sql
CREATE TABLE inventory (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  medicine_id UUID REFERENCES medicines(id),
  warehouse_id UUID REFERENCES warehouses(id),
  quantity INTEGER NOT NULL,
  batch_number VARCHAR(50),
  expiry_date DATE NOT NULL,
  reorder_level INTEGER DEFAULT 10,
  last_restocked TIMESTAMP,
  
  UNIQUE (medicine_id, warehouse_id, batch_number),
  INDEX idx_medicine (medicine_id),
  INDEX idx_warehouse (warehouse_id),
  INDEX idx_expiry (expiry_date)
);
```

**Orders Table**:
```sql
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_number VARCHAR(50) UNIQUE NOT NULL,
  patient_id UUID REFERENCES patients(id),
  prescription_id UUID REFERENCES prescriptions(id),
  order_type VARCHAR(20) NOT NULL, -- 'MEDICINE' or 'LAB'
  items JSONB NOT NULL,
  pricing JSONB NOT NULL,
  delivery_address JSONB NOT NULL,
  payment_id UUID,
  payment_status VARCHAR(20),
  order_status VARCHAR(50),
  warehouse_id UUID,
  delivery_partner_id UUID,
  tracking_url TEXT,
  estimated_delivery TIMESTAMP,
  delivered_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_patient (patient_id),
  INDEX idx_order_number (order_number),
  INDEX idx_status (order_status),
  INDEX idx_created (created_at DESC)
);
```

**Lab Bookings Table**:
```sql
CREATE TABLE lab_bookings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  booking_number VARCHAR(50) UNIQUE NOT NULL,
  patient_id UUID REFERENCES patients(id),
  consultation_id UUID REFERENCES consultations(id),
  lab_partner_id UUID REFERENCES lab_partners(id),
  tests JSONB NOT NULL,
  collection_type VARCHAR(20),
  collection_address JSONB,
  scheduled_slot TIMESTAMP,
  pricing JSONB NOT NULL,
  payment_id UUID,
  payment_status VARCHAR(20),
  booking_status VARCHAR(50),
  partner_booking_id VARCHAR(100),
  report_id UUID,
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_patient (patient_id),
  INDEX idx_booking_number (booking_number),
  INDEX idx_status (booking_status),
  INDEX idx_scheduled (scheduled_slot)
);
```

**Lab Reports Table**:
```sql
CREATE TABLE lab_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  booking_id UUID REFERENCES lab_bookings(id),
  patient_id UUID REFERENCES patients(id),
  test_results JSONB NOT NULL,
  file_url TEXT NOT NULL,
  ai_analysis JSONB,
  uploaded_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_booking (booking_id),
  INDEX idx_patient (patient_id),
  INDEX idx_uploaded (uploaded_at DESC)
);
```

**Payments Table**:
```sql
CREATE TABLE payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID REFERENCES patients(id),
  order_id UUID,
  amount DECIMAL(10, 2) NOT NULL,
  payment_type VARCHAR(20) NOT NULL,
  payment_method VARCHAR(50),
  razorpay_order_id VARCHAR(100),
  razorpay_payment_id VARCHAR(100),
  status VARCHAR(20) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  
  INDEX idx_patient (patient_id),
  INDEX idx_order (order_id),
  INDEX idx_status (status)
);
```

### MongoDB Collections (Document Store)

**Consultation Messages**:
```javascript
{
  _id: ObjectId,
  consultationId: UUID,
  messages: [
    {
      role: "user" | "assistant",
      content: String,
      audioUrl: String, // if voice input
      timestamp: Date
    }
  ],
  createdAt: Date,
  updatedAt: Date
}
```

**Product Reviews**:
```javascript
{
  _id: ObjectId,
  medicineId: UUID,
  patientId: UUID,
  rating: Number, // 1-5
  review: String,
  verified: Boolean, // purchased from platform
  createdAt: Date
}
```

**Lab Partner Data**:
```javascript
{
  _id: ObjectId,
  partnerId: UUID,
  name: String,
  accreditation: [String],
  rating: Number,
  servicedPincodes: [String],
  availableTests: [
    {
      testId: UUID,
      price: Number,
      reportTime: String
    }
  ],
  homeCollectionSlots: [
    {
      date: Date,
      slots: [String]
    }
  ],
  labLocations: [
    {
      address: String,
      pincode: String,
      coordinates: { lat: Number, lng: Number }
    }
  ]
}
```

---

## Technology Stack

### Frontend
- **Framework**: React 18 + TypeScript
- **State Management**: Redux Toolkit + RTK Query
- **UI Library**: Material-UI (MUI) or Ant Design
- **Mobile**: React Native (future)
- **Build Tool**: Vite

### Backend
- **Language**: Node.js + TypeScript
- **Framework**: NestJS (structured, scalable)
- **API**: REST + GraphQL (for complex queries)
- **Authentication**: JWT + Passport.js
- **Validation**: Zod or Joi

### Databases
- **Relational**: PostgreSQL 14 (AWS RDS)
- **Document**: MongoDB Atlas
- **Cache**: Redis (AWS ElastiCache)
- **Search**: Elasticsearch (for medicine catalog)

### Cloud Infrastructure (AWS)
- **Compute**: ECS Fargate
- **API Gateway**: AWS API Gateway
- **Storage**: S3 (prescriptions, reports)
- **CDN**: CloudFront
- **Functions**: Lambda (async tasks)
- **Queue**: SQS (order processing)

### External Services
- **AI**: OpenAI GPT-4 API
- **Payment**: Razorpay
- **SMS**: AWS SNS or Twilio
- **Email**: AWS SES
- **Maps**: Google Maps API (delivery tracking)
- **Analytics**: Mixpanel or Amplitude

---

## User Journeys

### Journey 1: Complete Healthcare Flow

```
Step 1: Patient feels unwell
    ↓
Step 2: Opens app, starts AI consultation
    ↓
Step 3: Chats with AI (3-5 minutes)
    ↓
Step 4: Receives AI-generated prescription
    ↓
Step 5: One-click "Order Medicines" from prescription
    ↓
Step 6: Reviews cart, selects generic alternatives if desired
    ↓
Step 7: Proceeds to checkout, pays ₹350
    ↓
Step 8: AI suggests relevant lab tests (e.g., "Consider CBC test")
    ↓
Step 9: Patient books lab test for ₹200
    ↓
Step 10: Schedules home collection for next morning
    ↓
Step 11: Pays ₹200 for lab test
    ↓
Step 12: Receives medicine delivery in 1 hour
    ↓
Step 13: Lab technician collects sample next day
    ↓
Step 14: Receives report via app in 24 hours
    ↓
Step 15: AI analyzes report, provides summary
    ↓
Step 16: Follow-up consultation if needed (free or discounted)

Total Time: 10 minutes (excluding delivery wait)
Total Cost: ₹50 (consultation) + ₹350 (medicines) + ₹200 (lab) = ₹600
```

### Journey 2: Repeat Prescription Refill

```
Step 1: Patient needs medicine refill
    ↓
Step 2: Opens app, goes to "Past Prescriptions"
    ↓
Step 3: Selects previous prescription
    ↓
Step 4: Clicks "Reorder Medicines"
    ↓
Step 5: Auto-filled cart, checkout
    ↓
Step 6: Delivery in 1 hour

Time: 2 minutes
```

### Journey 3: Preventive Health Checkup

```
Step 1: Patient wants health checkup
    ↓
Step 2: Opens "Lab Tests" section
    ↓
Step 3: Browses popular packages (Annual, Diabetes, Thyroid)
    ↓
Step 4: Selects "Complete Health Checkup" (₹1,299)
    ↓
Step 5: Chooses lab partner and home collection
    ↓
Step 6: Schedules convenient time slot
    ↓
Step 7: Pays and confirms
    ↓
Step 8: Sample collected at home
    ↓
Step 9: Reports uploaded in 48 hours
    ↓
Step 10: AI highlights abnormal values
    ↓
Step 11: Recommends follow-up consultation if needed
```

---

## Integration Workflows

### Workflow 1: Prescription → Medicine Order

```typescript
async function prescriptionToOrder(prescriptionId: string, patientId: string) {
  // 1. Fetch prescription
  const prescription = await getPrescription(prescriptionId);
  
  // 2. Create cart from prescribed medicines
  const cart = await createCartFromPrescription(prescription);
  
  // 3. Check inventory availability
  for (const item of cart.items) {
    const availability = await checkInventory(
      item.medicineId,
      item.quantity,
      patient.defaultAddress.pincode
    );
    
    if (!availability.available) {
      // Find alternatives
      item.alternatives = await findAlternatives(item.medicineId);
    }
  }
  
  // 4. Calculate pricing
  const pricing = await calculatePricing(cart);
  
  // 5. Show cart to patient with one-click checkout
  return {
    cart,
    pricing,
    quickCheckoutAvailable: true
  };
}
```

### Workflow 2: Consultation → Lab Recommendation

```typescript
async function recommendLabTests(consultation: Consultation) {
  const diagnosis = consultation.prescription.diagnosis;
  const symptoms = consultation.extractedData.symptoms;
  
  // AI recommends tests
  const recommendations = await aiRecommendLabTests(diagnosis, symptoms);
  
  // Match with available tests
  const tests = await getLabTests(recommendations.testNames);
  
  // Find affordable labs in patient's area
  const labs = await getLabPartners(patient.defaultAddress.pincode);
  
  // Show as post-consultation suggestion
  return {
    message: "Based on your consultation, these tests are recommended:",
    tests: tests.map(t => ({
      name: t.name,
      price: t.price,
      labs: labs.filter(l => l.availableTests.includes(t.id))
    }))
  };
}
```

### Workflow 3: Lab Report → Follow-up Consultation

```typescript
async function analyzeReportAndSuggestFollowup(reportId: string) {
  const report = await getLabReport(reportId);
  
  // AI analyzes report
  const analysis = await aiAnalyzeReport(report);
  
  if (analysis.severity === 'ATTENTION_NEEDED' || analysis.severity === 'URGENT') {
    // Auto-suggest follow-up consultation
    await notificationService.sendPush(report.patientId, {
      title: "Lab Report Ready",
      body: "Your report shows some abnormal values. We recommend a follow-up consultation.",
      action: {
        type: "START_CONSULTATION",
        discount: 50 // 50% off for follow-up
      }
    });
  }
  
  return analysis;
}
```

---

## Cost Estimation & Pricing

### Infrastructure Costs (Monthly at 10K consultations/day)

| Component | Specification | Monthly Cost |
|-----------|--------------|--------------|
| **Compute** | | |
| ECS Fargate | 4 tasks × 2 vCPU × 4GB | $200 |
| Lambda Functions | 5M invocations | $50 |
| **Database** | | |
| RDS PostgreSQL | db.t3.large Multi-AZ | $200 |
| MongoDB Atlas | M10 cluster | $100 |
| Redis Cache | cache.t3.medium | $75 |
| **Storage** | | |
| S3 Storage | 500GB | $12 |
| CloudFront | 2TB transfer | $150 |
| **Search** | | |
| Elasticsearch | 3-node cluster | $150 |
| **Misc** | | |
| API Gateway | 50M requests | $50 |
| CloudWatch | Logs + Metrics | $50 |
| **AWS Total** | | **$1,037** |
| | | |
| **External Services** | | |
| OpenAI API | 300K consultations | $24,000 |
| Razorpay | 2.5% on ₹40M GMV | $24,000 |
| SMS | 900K messages × $0.01 | $9,000 |
| **External Total** | | **$57,000** |
| | | |
| **TOTAL MONTHLY** | | **$58,037** |

### Revenue Model (Monthly at 10K/day)

**Consultation Revenue**:
- 300,000 consultations × ₹50 = ₹15M ($180K)

**Medicine Sales**:
- 70% conversion × 300K = 210,000 orders
- Average order: ₹400
- Revenue: ₹84M ($1M)
- Margin: 20% = ₹16.8M ($200K)

**Lab Bookings**:
- 30% take rate × 300K = 90,000 bookings
- Average booking: ₹600
- Revenue: ₹54M ($648K)
- Commission: 15% = ₹8.1M ($97.2K)

**Total Monthly Revenue**: $1.83M
**Total Monthly Costs**: $58K
**Gross Profit**: $1.77M (97% margin)
**Operating Costs** (team, marketing): ~$500K
**Net Profit**: ~$1.27M (69% margin)

---

## Security & Compliance

### Data Security
1. **Encryption**:
   - TLS 1.3 for all data in transit
   - AES-256 encryption for data at rest
   - Patient health data encrypted at field level

2. **Access Control**:
   - Role-based access (Patient, Admin, Warehouse, Lab Partner)
   - JWT tokens with 15-minute expiry
   - API rate limiting: 100 req/min per user

3. **PII Protection**:
   - Personal Identifiable Information masked in logs
   - Secure storage of Aadhaar/PAN (if collected)
   - GDPR-like data deletion rights

### Compliance
1. **Medical Regulations**:
   - Electronic prescription format compliance
   - Drug schedule tracking (H, H1, X substances)
   - Prescription validity enforcement

2. **E-Commerce Regulations**:
   - GST calculation and invoicing
   - Return/refund policy enforcement
   - Consumer protection compliance

3. **Data Protection**:
   - Consent management
   - Data retention policies (7 years for medical records)
   - Audit trails for all data access

---

## Monitoring & Operations

### Key Metrics Dashboard

**Health Metrics**:
- API response times (p50, p95, p99)
- Error rates by service
- OpenAI API latency and failures
- Database query performance

**Business Metrics**:
- Daily consultations
- Prescription-to-order conversion rate
- Average order value
- Lab booking rate
- Customer lifetime value

**Operational Metrics**:
- Inventory levels by warehouse
- Order fulfillment time
- Medicine delivery SLA compliance
- Lab report turnaround time

### Alerting

**Critical Alerts**:
- OpenAI API failure (> 5%)
- Payment gateway down
- Inventory below reorder level
- Database connection failures

**Warning Alerts**:
- High API latency (> 3s)
- Low conversion rates
- Warehouse stock outs
- Lab partner SLA breach

---

## Implementation Roadmap

### Phase 1: MVP (Weeks 1-10)

**Weeks 1-3: Core Services**
- Patient service + authentication
- AI consultation service (basic)
- Medicine catalog (500 medicines)
- Basic order management

**Weeks 4-6: E-Commerce**
- Shopping cart + checkout
- Payment integration (Razorpay)
- Single warehouse inventory
- Order tracking

**Weeks 7-8: Lab Integration**
- Lab test catalog
- Partner integration (1-2 labs)
- Booking flow
- Report upload

**Weeks 9-10: Polish & Testing**
- End-to-end testing
- Security audit
- Load testing
- Beta launch

### Phase 2: Scale (Months 3-6)

- Multi-warehouse logistics
- Advanced AI features
- Medicine subscriptions
- Health records management
- Mobile app (React Native)
- 5+ lab partners
- Referral program

### Phase 3: Platform (Months 6-12)

- White-label solutions
- Corporate health plans
- Insurance integration
- Chronic disease management
- Telemedicine (video calls)
- Pharmacy franchising

---

## Conclusion

This integrated healthcare platform combines AI consultation, e-commerce, and lab services into a seamless experience. The architecture is designed for:

1. **Scalability**: Handle 10K+ daily consultations and orders
2. **Integration**: Seamless data flow between services
3. **Extensibility**: Easy to add new services (imaging, physiotherapy, etc.)
4. **Economics**: Strong unit economics with 69% net margin at scale
5. **User Experience**: 10-minute end-to-end healthcare journey

**Next Steps**:
1. Validate architecture with technical team
2. Finalize lab partner integrations
3. Build MVP in 10 weeks
4. Pilot with 100 users
5. Scale to production

**Key Success Factors**:
- AI prescription quality (>90% confidence)
- Fast medicine delivery (<2 hours)
- Reliable lab partners (>95% on-time)
- Competitive pricing (20% below market)
- Seamless user experience
