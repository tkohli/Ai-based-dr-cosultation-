# Complete Technical Flow Document
## Healthcare AI Platform - 45-Day MVP + Live Feature Rollout

---

## EXECUTIVE SUMMARY

**Mission**: Launch a fully functional AI-powered healthcare platform in 45 days, then continuously add features while live.

**MVP Scope (Day 1-45)**: Core consultation + prescription + pharmacy ordering + basic payments
**Live Feature Rollout (Day 46+)**: Advanced features, genetic testing, ads, family accounts

**Architecture Philosophy**: 
- Microservices from day 1 (easy to add features live)
- Feature flags for controlled rollouts
- Zero-downtime deployments
- Modular, independent services

---

## 45-DAY MVP DELIVERY PLAN

### PHASE 1: Foundation (Days 1-10)

**Week 1 (Days 1-5): Infrastructure Setup**

**Day 1-2: AWS Infrastructure**
```
Tasks:
✓ Set up AWS Organization + Multi-account structure
  - Production account
  - Development account
  - Staging account
✓ VPC setup with public/private subnets (3 AZs)
✓ RDS PostgreSQL Multi-AZ (db.t3.medium)
✓ ElastiCache Redis (cache.t3.small)
✓ S3 buckets (medical-records-prod, prescriptions-prod, avatars-prod)
✓ CloudFront distributions
✓ API Gateway setup
✓ Route 53 domain configuration
✓ AWS Secrets Manager for credentials
✓ KMS keys for encryption

Tech Stack:
- Infrastructure as Code: Terraform
- Repository: GitHub with branch protection
- CI/CD: GitHub Actions
```

**Day 3-5: Core Backend Services Setup**
```
✓ Backend monolith with modular structure (NestJS)
  /src
    /modules
      /auth
      /patients
      /consultations
      /prescriptions
      /pharmacy
      /payments
    /shared
      /database
      /config
      /utils

✓ Database schema v1.0
  - patients table
  - consultations table
  - prescriptions table
  - medicines table
  - orders table
  - payments table
  - audit_logs table

✓ Authentication service (AWS Cognito integration)
✓ Database migrations setup (Prisma)
✓ API documentation (Swagger)
✓ Logging setup (Winston + CloudWatch)
✓ Error tracking (Sentry)
```

**Week 2 (Days 6-10): AI Avatar + Core Frontend**

**Day 6-8: AI Avatar Integration**
```
✓ D-ID API integration for 3D avatar
✓ AWS Transcribe setup (STT)
✓ AWS Polly setup (TTS)
✓ WebRTC implementation for real-time audio
✓ Avatar conversation controller
✓ Session management for avatar state

Avatar Flow:
1. Patient clicks "Start Consultation"
2. Avatar appears with greeting
3. Patient speaks → AWS Transcribe → Text
4. Text → OpenAI (anonymized) → Response
5. Response → AWS Polly → Speech
6. Avatar lip-syncs to speech (D-ID)
7. Repeat until consultation complete
```

**Day 9-10: Frontend Foundation**
```
✓ React app setup (Vite + TypeScript)
✓ Component library (Material-UI)
✓ State management (Redux Toolkit)
✓ Routing (React Router)
✓ API client (Axios + RTK Query)
✓ Authentication flow
✓ Avatar consultation UI
✓ Responsive design (mobile-first)

Pages (MVP):
- Login/Registration
- Patient Dashboard
- Avatar Consultation
- Prescription View
- Pharmacy Browse
- Cart & Checkout
- Order Tracking
```

---

### PHASE 2: Core Features (Days 11-30)

**Week 3 (Days 11-15): RAG Privacy Layer + OpenAI Integration**

**Day 11-12: RAG Implementation**
```
✓ Vector database setup (Pinecone)
✓ Medical knowledge base embedding
  - 100 common conditions
  - 500 medicines database
  - Treatment protocols

✓ PHI stripping service
  Input: "My name is Rajesh, I have fever"
  Output (to LLM): "Patient has fever"
  
✓ Anonymization rules engine
  - Remove: names, phone, address, DOB
  - Keep: age bracket, symptoms, medical history
  - Token replacement for tracking

✓ Medical knowledge retrieval
  Symptoms → Embedding → Vector search → Relevant protocols
```

**Day 13-15: OpenAI Integration + Prescription Generation**
```
✓ OpenAI API wrapper service
✓ Conversation management
  - Session state tracking
  - Context window management
  - Token optimization

✓ System prompt engineering
✓ Prescription generation logic
✓ Safety validation rules
  - Emergency detection
  - Controlled substance blocking
  - Drug interaction checking

Prescription Generation Flow:
1. Avatar gathers symptoms (5-10 exchanges)
2. Extract structured data
3. Call OpenAI with medical context
4. Generate prescription JSON
5. Validate against safety rules
6. Store as DRAFT status
7. Assign to physician queue
```

**Week 4 (Days 16-20): Physician Review Portal**

**Day 16-18: Physician Dashboard**
```
✓ Physician login (separate Cognito pool)
✓ Pending consultation queue
✓ Consultation detail view with full transcript
✓ Prescription edit interface
✓ Approve/Reject workflow
✓ Physician notes field
✓ Real-time queue updates (Server-Sent Events)

Dashboard Features:
- Queue sorted by urgency
- Consultation filters (urgent, routine)
- Search by patient name/ID
- Performance metrics (avg review time)
```

**Day 19-20: Digital Signature Integration**
```
✓ Aadhaar eSign API integration (e-Mudhra/NSDL)
✓ Signature capture workflow
✓ PDF generation with signature
✓ Signature verification
✓ Immutable audit trail

eSign Flow:
1. Physician clicks "Approve"
2. System generates prescription PDF
3. eSign API called with Aadhaar OTP
4. Physician enters OTP
5. Digital signature applied to PDF
6. PDF stored in S3 with signature hash
7. Prescription marked APPROVED
8. Patient notified
```

**Week 5 (Days 21-25): Pharmacy Marketplace**

**Day 21-22: Medicine Catalog**
```
✓ Medicine database (1000+ common medicines)
  - Name, generic name, manufacturer
  - MRP, selling price, discount
  - Images, descriptions
  - Stock levels
  - Prescription requirement flag

✓ Search & filter APIs
✓ Category browse
✓ Generic alternatives suggestion
✓ Inventory management system
```

**Day 23-25: Order Management**
```
✓ Shopping cart service
✓ Prescription-to-cart conversion
✓ Address management
✓ Order creation workflow
✓ Order status tracking
✓ Delivery partner integration (Dunzo/Porter API)

Order States:
PLACED → CONFIRMED → PACKED → SHIPPED → OUT_FOR_DELIVERY 
→ DELIVERED (OTP verified) → COMPLETED

✓ Pharmacy partner dashboard (basic)
  - New orders notification
  - Order acceptance/rejection
  - Stock updates
  - Packing confirmation
```

---

### PHASE 3: Payments (Days 26-35)

**Week 6 (Days 26-30): Core Payment Integration**

**Day 26-28: Razorpay Integration**
```
✓ Razorpay account setup + API keys
✓ Payment gateway service
✓ Order payment flow
  - Create Razorpay order
  - Payment link generation
  - Webhook handling (success/failure)
  - Payment verification

✓ Payment methods supported:
  - UPI
  - Credit/Debit cards
  - Netbanking
  - Wallets (Paytm, PhonePe, etc.)

✓ Refund workflow (for order cancellations)
```

**Day 29-30: Basic Wallet System**
```
✓ Wallet ledger table
  - patient_id
  - transaction_type (CREDIT/DEBIT)
  - amount
  - balance_after
  - reference_id
  - timestamp

✓ Wallet APIs
  - Get balance
  - Add money (Razorpay)
  - Deduct for purchases
  - Transaction history

✓ Wallet payment option in checkout
✓ Auto-debit preference

Note: Full PPI compliance deferred to post-MVP
Interim: Partner with licensed PPI provider (Paytm/PhonePe)
```

**Week 7 (Days 31-35): OTP-on-Delivery + Patient Signature**

**Day 31-33: OTP-on-Delivery Payment Release**
```
✓ OTP generation service (Redis + TTL)
✓ SMS integration (MSG91)
✓ Delivery partner app mock
✓ OTP verification endpoint
✓ Payment release logic

Flow:
1. Order reaches customer
2. System generates 6-digit OTP
3. SMS sent to patient
4. Delivery person asks for OTP
5. Patient provides OTP
6. Delivery person enters in app
7. Server verifies OTP
8. If valid: Release payment to merchant
9. Mark order COMPLETED
```

**Day 34-35: Patient Digital Signature (NEW)**
```
✓ Signature pad component (React)
✓ Signature capture API
✓ Signature storage (S3 as image)
✓ Consent logging

Signature Trigger Points:
1. Before viewing final prescription
2. Before genetic test consent
3. Before sharing medical records via QR

Tech Implementation:
import SignatureCanvas from 'react-signature-canvas';

const handleSignature = async () => {
  const signatureDataURL = sigPad.toDataURL();
  await api.submitSignature({
    prescriptionId,
    signatureData: signatureDataURL,
    timestamp: new Date().toISOString(),
    ipAddress: getUserIP()
  });
};

Backend:
- Store signature image in S3
- Save metadata (prescription_id, timestamp, IP) in DB
- Generate signature hash (SHA-256)
- Link to prescription record
- Immutable audit log entry
```

---

### PHASE 4: Testing & Launch (Days 36-45)

**Week 8 (Days 36-40): Integration Testing**

**Day 36-38: End-to-End Testing**
```
✓ Complete user flow testing
  1. Patient registration
  2. Avatar consultation (20 test cases)
  3. Prescription generation
  4. Physician review
  5. Patient signature
  6. Medicine ordering
  7. Payment (test mode)
  8. OTP delivery verification

✓ Edge cases
  - Network failures
  - OpenAI API timeout
  - Payment failures
  - Concurrent consultations
  - Invalid prescriptions

✓ Load testing (Artillery/JMeter)
  - 100 concurrent consultations
  - 500 medicine searches/min
  - 50 simultaneous checkouts
```

**Day 39-40: Security Audit**
```
✓ OWASP ZAP scan
✓ Penetration testing
✓ PHI encryption verification
✓ Access control testing
✓ API rate limiting validation
✓ SQL injection prevention
✓ XSS vulnerability check
✓ CSRF protection
✓ Session management review
```

**Week 9 (Days 41-45): Staging + Soft Launch**

**Day 41-42: Staging Deployment**
```
✓ Staging environment setup (identical to prod)
✓ Full deployment rehearsal
✓ Smoke tests on staging
✓ UAT with 10 beta users
✓ Performance monitoring
✓ Error tracking verification
```

**Day 43-44: Production Deployment**
```
✓ Database migration (production)
✓ Application deployment
  - Blue-Green deployment strategy
  - Health check verification
  - Smoke tests
  - Rollback plan ready

✓ DNS cutover
✓ SSL certificate verification
✓ CDN cache warmup
✓ Monitoring alerts setup
```

**Day 45: Soft Launch**
```
✓ Launch to 100 users (controlled)
✓ Monitor metrics
  - API response times
  - Error rates
  - Consultation completion rate
  - Payment success rate
✓ Support team ready
✓ Incident response plan active
```

---

## MVP FEATURE CHECKLIST (Day 45)

**✓ Must-Have (Launched)**
- [x] Patient registration (OTP-based)
- [x] AI Avatar consultation (text + voice)
- [x] RAG privacy layer
- [x] Prescription generation
- [x] Physician review + eSign
- [x] Patient signature before prescription
- [x] Medicine catalog (1000 medicines)
- [x] Shopping cart + checkout
- [x] Razorpay payment integration
- [x] Basic wallet (add money + pay)
- [x] OTP-on-delivery
- [x] Order tracking
- [x] SMS notifications
- [x] Admin dashboard (basic)

**⏳ Nice-to-Have (Deferred)**
- [ ] Lab test ordering
- [ ] Family accounts
- [ ] QR-based sharing
- [ ] Genetic testing
- [ ] Advertisements
- [ ] Advanced analytics
- [ ] Mobile app (React Native)

---

## LIVE FEATURE ROLLOUT STRATEGY (Day 46+)

### Philosophy: Ship Small, Ship Often

**Deployment Strategy**:
1. **Feature Flags**: All new features behind flags (LaunchDarkly/Unleash)
2. **Canary Releases**: 5% → 25% → 50% → 100%
3. **A/B Testing**: Compare new features with control group
4. **Zero Downtime**: Blue-green deployments
5. **Instant Rollback**: If error rate > 1%, auto-rollback

---

### Sprint 1 (Week 10-11): Lab Testing Module

**Day 46-50: Lab Partner Integration**
```
New Services:
- Lab catalog service
- Lab booking service
- Partner API adapters (Thyrocare, Dr. Lal PathLabs)

Database Changes (Migration):
CREATE TABLE lab_tests (
  id UUID PRIMARY KEY,
  name VARCHAR(200),
  category VARCHAR(100),
  description TEXT,
  price DECIMAL(10,2),
  report_time VARCHAR(50)
);

CREATE TABLE lab_bookings (
  id UUID PRIMARY KEY,
  patient_id UUID,
  tests JSONB,
  collection_type VARCHAR(20),
  scheduled_slot TIMESTAMP,
  status VARCHAR(50)
);

Deployment:
1. Deploy new tables (migration)
2. Deploy lab service (feature flag OFF)
3. Test in production (internal users only)
4. Enable feature flag for 5% users
5. Monitor for 48 hours
6. Gradual rollout to 100%
```

**Day 51-55: Lab UI + Booking Flow**
```
Frontend Changes:
- New "Lab Tests" tab in dashboard
- Test catalog page
- Booking flow
- Home collection scheduling
- Report viewer

Deployment:
- Deploy frontend build to S3
- CloudFront cache invalidation
- Feature flag: lab_tests_enabled
- Rollout: 10% → 50% → 100%
```

---

### Sprint 2 (Week 12-13): Family Accounts

**Day 56-60: Multi-Account Management**
```
Database Changes:
CREATE TABLE family_accounts (
  id UUID PRIMARY KEY,
  owner_id UUID REFERENCES patients(id),
  member_id UUID REFERENCES patients(id),
  relationship VARCHAR(50),
  access_level VARCHAR(20), -- OWNER, MANAGER, VIEWER
  consent_timestamp TIMESTAMP
);

CREATE TABLE family_invites (
  id UUID PRIMARY KEY,
  inviter_id UUID,
  invitee_phone VARCHAR(15),
  invite_code VARCHAR(10),
  status VARCHAR(20),
  expires_at TIMESTAMP
);

Backend Services:
- Family account service
- Invitation management
- Consent tracking
- Access control middleware

APIs:
POST   /api/v1/family/invite
GET    /api/v1/family/members
POST   /api/v1/family/accept-invite
DELETE /api/v1/family/remove-member
GET    /api/v1/family/member/:id/consultations
```

**Day 61-65: Family UI**
```
Frontend:
- Family management dashboard
- Add member flow
- Member profile switching
- Consent capture UI

Deployment:
- Database migration (zero-downtime)
- Backend deployment (new APIs)
- Frontend deployment (feature flagged)
- Rollout: 5% → 100% over 5 days
```

---

### Sprint 3 (Week 14-15): QR Medical Sharing

**Day 66-70: QR Generation + Secure Viewer**
```
New Services:
- QR token service (JWT with expiry)
- Medical record access service
- OTP validation service

Tech Stack:
- QR library: qrcode.react
- JWT library: jsonwebtoken
- Encryption: AES-256

QR Flow:
1. Patient selects records to share
2. System generates encrypted JWT
   - Contains: record IDs, scope, expiry (1 hour)
   - Signed with app secret
3. JWT encoded in QR code
4. Recipient scans QR
5. System prompts for OTP
6. OTP sent to patient's phone
7. Patient shares OTP with recipient
8. Recipient enters OTP
9. System validates + shows records
10. Access logged in audit trail

Implementation:
const generateShareToken = (patientId, recordIds, ttl) => {
  return jwt.sign(
    {
      patientId,
      recordIds,
      scope: 'medical_share',
      exp: Date.now() + ttl
    },
    JWT_SECRET
  );
};

const qrData = JSON.stringify({
  type: 'MEDICAL_SHARE',
  token: shareToken,
  appUrl: 'https://app.healthcare.com/share'
});

<QRCode value={qrData} size={256} />
```

**Day 71-75: QR Scanning + Viewer UI**
```
Frontend:
- QR generator page
- QR scanner (using device camera)
- OTP entry modal
- Secure medical viewer
- Access time limit countdown

Mobile Support:
- Camera permission handling
- QR detection (react-qr-scanner)
- Deep linking to app
```

---

### Sprint 4 (Week 16-17): Patient Identity Verification (NEW)

**Day 76-80: Aadhaar Linking (Optional)**
```
Purpose: Enable higher-trust workflows

Integration:
- Aadhaar eKYC provider (Surepass/AuthBridge)
- Document upload service
- OCR service (AWS Textract)
- Identity verification microservice

Database:
CREATE TABLE patient_identities (
  id UUID PRIMARY KEY,
  patient_id UUID REFERENCES patients(id),
  identity_type VARCHAR(20), -- AADHAAR, PAN, PASSPORT
  identity_number_hash VARCHAR(64), -- SHA-256 hash
  verification_status VARCHAR(20),
  verified_at TIMESTAMP,
  expiry_date DATE,
  kyc_provider VARCHAR(50),
  kyc_reference_id VARCHAR(100)
);

Flow:
1. Patient clicks "Verify Identity"
2. Chooses document type (Aadhaar/PAN)
3. For Aadhaar:
   a. Enter Aadhaar number
   b. OTP sent by UIDAI
   c. Patient enters OTP
   d. eKYC data received
   e. Name, DOB, Photo extracted
   f. Stored encrypted
4. For other documents:
   a. Upload image
   b. OCR extraction
   c. Manual verification (admin)

Benefits Unlocked:
- Genetic testing access
- Higher purchase limits
- Premium features
- Digital signature on important documents
```

**Day 81-85: Verification UI + Badge System**
```
Frontend:
- Identity verification flow
- Document upload widget
- Verification status badge
- Feature gating based on verification

UI Changes:
- "Verified" badge on profile
- Unlock indicator for genetic tests
- Trust score display
```

---

### Sprint 5 (Week 18-19): Genetic Testing Module

**Day 86-90: Genetic Lab Integration**
```
Special Requirements:
- Enhanced consent workflow
- Digital signature mandatory
- Extra privacy measures
- Specialized lab partner APIs

Database:
CREATE TABLE genetic_tests (
  id UUID PRIMARY KEY,
  patient_id UUID,
  test_type VARCHAR(100),
  consent_form_id UUID,
  digital_signature_url TEXT,
  kit_tracking_number VARCHAR(50),
  sample_collected_at TIMESTAMP,
  report_id UUID,
  status VARCHAR(50)
);

CREATE TABLE genetic_consents (
  id UUID PRIMARY KEY,
  patient_id UUID,
  test_id UUID,
  consent_text TEXT,
  signature_data TEXT,
  aadhaar_esign_ref VARCHAR(100),
  timestamp TIMESTAMP,
  ip_address INET,
  is_immutable BOOLEAN DEFAULT true
);

Consent Flow:
1. Patient selects genetic test
2. Required: Identity verified (Aadhaar)
3. Show detailed consent form
   - Purpose of test
   - Data usage policy
   - Storage duration
   - Sharing restrictions
   - Right to withdraw
4. Patient reads and scrolls through
5. Digital signature required
   - Aadhaar eSign (recommended)
   - Or manual signature pad
6. OTP confirmation
7. Consent stored immutably
8. Only then: Test kit ordered
```

**Day 91-95: Genetic Test UI + Report Viewer**
```
Frontend:
- Genetic test catalog (gated)
- Multi-step consent wizard
- Signature capture
- Kit tracking
- Encrypted report viewer
- Result interpretation guide

Security:
- Extra encryption layer for genetic data
- Access only with 2FA
- Auto-logout after 5 minutes
- No screenshots allowed (watermark)
```

---

### Sprint 6 (Week 20-21): Data Aggregation & Analytics

**Day 96-100: De-identified Data Pipeline**
```
Purpose: Create non-PII dataset for insights/ads

Architecture:
Patient Data (PHI) → Anonymization Service → Aggregated Data Lake

ETL Pipeline:
1. Lambda triggered daily (cron)
2. Extract consultation data
3. Strip all PII:
   - Remove: name, phone, email, address
   - Generalize: age → age bracket (18-25, 26-35)
   - Generalize: pincode → city/state only
   - Remove: exact timestamps → month/year only
4. Aggregate over cohorts (min 100 patients)
5. Store in Redshift/BigQuery

Tech Stack:
- AWS Glue / Lambda for ETL
- Data pipeline: Apache Airflow
- Storage: AWS Redshift
- BI: AWS QuickSight

Example Aggregation:
Instead of:
"Rajesh, age 45, Delhi-110025, fever on 2025-01-15"

Aggregated:
"Age 40-50, North India, January 2025, fever: 1234 cases"

Differential Privacy:
- Add noise to small cohorts
- Suppress data if cohort < 100
- No re-identification possible
```

**Day 101-105: Analytics Dashboard (Internal)**
```
Dashboards:
1. Health Trends Dashboard
   - Top symptoms by region
   - Seasonal patterns
   - Medication prescribing patterns

2. Business Intelligence
   - Consultation volume trends
   - Conversion funnels
   - Average order value
   - Lab test popularity

3. Ad Targeting Segments
   - Age brackets
   - Region
   - Health condition categories (broad)
   - No individual targeting
```

---

### Sprint 7 (Week 22-23): Advertisement System

**Day 106-110: Wait-Time Ad Module**
```
Purpose: Show ads during 30-second prescription processing

Architecture:
Frontend → Ad Service → Ad Content (S3 / Ad Network API)

Database:
CREATE TABLE ads (
  id UUID PRIMARY KEY,
  title VARCHAR(100),
  description TEXT,
  image_url TEXT,
  click_url TEXT,
  category VARCHAR(50),
  target_regions TEXT[],
  target_age_brackets VARCHAR(20)[],
  start_date DATE,
  end_date DATE,
  is_active BOOLEAN
);

CREATE TABLE ad_impressions (
  id UUID PRIMARY KEY,
  ad_id UUID,
  patient_id UUID,
  shown_at TIMESTAMP,
  clicked BOOLEAN,
  clicked_at TIMESTAMP
);

Ad Service Logic:
1. Patient waits for prescription
2. Ad service API called
3. Filters:
   - Active ads only
   - Matches patient region (anonymized)
   - Matches age bracket
   - Category relevance (health/wellness)
4. Returns ad content
5. Frontend shows ad (bottom 20% of screen)
6. Tracks impression + clicks

Frontend Implementation:
const WaitingAd = () => {
  const [ad, setAd] = useState(null);
  
  useEffect(() => {
    adService.fetchAd({
      region: user.region,
      agebracket: user.agebracket
    }).then(setAd);
  }, []);
  
  return (
    <div className="waiting-ad">
      <img src={ad.imageUrl} />
      <a href={ad.clickUrl} onClick={trackClick}>
        {ad.title}
      </a>
    </div>
  );
};

Compliance:
- No health-related product ads (drugs, devices)
- Only wellness/lifestyle ads
- Clear "Ad" label
- Opt-out available in settings
```

**Day 111-115: Ad Management Portal**
```
Admin Features:
- Upload ads (image, title, CTA)
- Set targeting parameters
- Schedule campaigns
- View performance metrics
- Pause/resume campaigns

Analytics:
- Impressions count
- Click-through rate
- Conversion tracking (if integrated with advertisers)
```

---

### Sprint 8 (Week 24): Push Notifications & Promotions

**Day 116-120: Promotional Pop-Up System**
```
Purpose: Re-engage users with new offers/features

Tech Stack:
- Firebase Cloud Messaging (FCM)
- In-app modal system
- Push scheduler service (AWS EventBridge)

Database:
CREATE TABLE promotions (
  id UUID PRIMARY KEY,
  title VARCHAR(100),
  message TEXT,
  image_url TEXT,
  deep_link VARCHAR(200),
  target_audience JSONB,
  start_date TIMESTAMP,
  end_date TIMESTAMP,
  priority INTEGER
);

CREATE TABLE push_logs (
  id UUID PRIMARY KEY,
  patient_id UUID,
  promotion_id UUID,
  sent_at TIMESTAMP,
  delivered BOOLEAN,
  clicked BOOLEAN
);

Promotion Triggers:
1. New feature launch
2. Discount offers
3. Health checkup reminders
4. Lab test promotions
5. Abandoned cart recovery

User Preferences:
CREATE TABLE notification_preferences (
  patient_id UUID PRIMARY KEY,
  promotional_push BOOLEAN DEFAULT true,
  promotional_email BOOLEAN DEFAULT true,
  health_tips BOOLEAN DEFAULT true,
  order_updates BOOLEAN DEFAULT true -- Always true
);

Frontend:
- Preference center in settings
- In-app notification center
- Deep link handling

Implementation:
// Backend: Send push
await fcmService.send({
  patientId: 'uuid',
  title: 'New Lab Tests Available',
  body: '20% off on full body checkup',
  deepLink: '/lab-tests/checkup',
  imageUrl: 'https://cdn.../promo.jpg'
});

// Frontend: Handle notification
messaging.onMessage((payload) => {
  showInAppModal({
    title: payload.notification.title,
    message: payload.notification.body,
    cta: payload.data.deepLink
  });
});
```

---

## LIVE DEPLOYMENT TECHNICAL DEEP DIVE

### Architecture for Zero-Downtime Deployments

**1. Blue-Green Deployment Strategy**

```
Current Setup:
┌─────────────────────────────────────────┐
│         Load Balancer (ALB)             │
│  (Routes 100% traffic to Blue)          │
└───────────┬─────────────────────────────┘
            │
    ┌───────▼────────┐        ┌─────────────────┐
    │  Blue (Live)   │        │  Green (Idle)   │
    │  Version 1.0   │        │  Version 1.1    │
    │  10 instances  │        │  0 instances    │
    └────────────────┘        └─────────────────┘

Deployment Process:
Step 1: Provision Green environment
  - Launch 10 new ECS tasks with v1.1
  - Health checks: All pass
  
Step 2: Smoke tests on Green
  - Automated: API health checks
  - Manual: QA team verifies critical paths
  
Step 3: Gradual traffic shift
  - ALB: 5% → Green, 95% → Blue (5 minutes)
  - Monitor: Error rate, latency, success rate
  - ALB: 25% → Green, 75% → Blue (10 minutes)
  - Monitor again
  - ALB: 50% → Green, 50% → Blue (15 minutes)
  - ALB: 100% → Green (if all metrics green)
  
Step 4: Monitor for 1 hour
  - If error rate > 1% or latency > 3s:
    → Instant rollback (flip to Blue)
  - If stable:
    → Terminate Blue instances
    → Green becomes new Blue

Rollback SLA: < 30 seconds
```

**2. Database Migrations (Zero-Downtime)**

**Challenge**: Adding new columns while app is live

**Solution**: Backwards-compatible migrations in stages

```
Example: Adding 'family_account_id' column

Stage 1 (Deploy Week 1):
- Add column as NULLABLE
ALTER TABLE patients ADD COLUMN family_account_id UUID NULL;
- Old code: Doesn't use this column (works fine)
- New code: Can read/write this column
- Both versions coexist

Stage 2 (Deploy Week 2):
- Backfill data (background job)
UPDATE patients SET family_account_id = ... WHERE ...;
- Old code: Still works (ignores column)
- New code: Uses column

Stage 3 (Deploy Week 3):
- Add NOT NULL constraint (if required)
ALTER TABLE patients ALTER COLUMN family_account_id SET NOT NULL;
- By now, all instances are new code only
```

**Key Rules**:
1. Never drop columns immediately (wait 2 versions)
2. Always add columns as nullable first
3. Use feature flags to enable new features
4. Backward-compatible API changes only

**3. Feature Flags Implementation**

**Tech**: LaunchDarkly (SaaS) or Unleash (self-hosted)

```typescript
// Backend
import { LaunchDarkly } from 'launchdarkly-node-server-sdk';

const client = LaunchDarkly.init(LAUNCHDARKLY_SDK_KEY);

// Check feature flag
const labTestsEnabled = await client.variation(
  'lab-tests-feature',
  { key: patientId, custom: { region: 'bangalore' } },
  false // default if flag fetch fails
);

if (labTestsEnabled) {
  // Show lab tests
} else {
  // Hide lab tests
}

// Frontend
import { useLDClient } from 'launchdarkly-react-client-sdk';

const MyComponent = () => {
  const ldClient = useLDClient();
  const labTestsEnabled = ldClient.variation('lab-tests-feature', false);
  
  return labTestsEnabled ? <LabTests /> : null;
};
```

**Flag Rollout Strategy**:
```
1. Create flag: lab-tests-feature (OFF)
2. Deploy code with flag check (production)
3. Enable for internal team (5 users)
4. Test thoroughly
5. Enable for 1% of users (geo-targeted)
6. Monitor for 24 hours
7. Gradual increase: 5% → 25% → 50% → 100%
8. Remove flag after 2 weeks of stable 100% rollout
```

**4. Canary Releases**

**What**: Deploy to small subset first, monitor, then gradually increase

```
Infrastructure:
┌─────────────────────────────────────────┐
│         Load Balancer (ALB)             │
└───────┬──────────────────┬──────────────┘
        │                  │
  ┌─────▼──────┐    ┌──────▼───────┐
  │   Stable   │    │   Canary     │
  │  Version   │    │   Version    │
  │  (95% )    │    │   (5%)       │
  └────────────┘    └──────────────┘

Traffic Splitting:
- Use ALB target groups
- Stable: 95% weight
- Canary: 5% weight

Canary Metrics (Automated):
- Error rate: < 1%
- Avg latency: < 2s
- Success rate: > 99%

If any metric fails:
→ Automatic rollback (set canary weight to 0%)
→ Alert engineering team
→ Investigate issue

If all metrics pass (after 1 hour):
→ Increase canary weight: 25% → 50% → 100%
```

**5. Database Replication & Read Replicas**

```
Setup:
┌──────────────────┐         ┌──────────────────┐
│  Primary (Write) │────────>│  Replica (Read)  │
│  RDS PostgreSQL  │  Async  │  RDS PostgreSQL  │
│  Multi-AZ        │  Repli  │  Read-only       │
└──────────────────┘  cation └──────────────────┘

Usage:
- All writes → Primary
- Heavy reads (analytics, reports) → Replica
- App reads → Primary (for consistency)

Benefits:
- Offload heavy queries
- HA: If primary fails, promote replica
- Zero downtime upgrades:
  1. Upgrade replica
  2. Failover to replica
  3. Replica becomes primary
  4. Old primary becomes new replica
  5. Upgrade old primary
```

**6. Cache Invalidation Strategy**

**Challenge**: New code deployed, but Redis has old data

**Solution**: Cache versioning

```typescript
// Old approach (problematic):
redis.get('patient:uuid123'); // Returns v1 data

// New approach (versioned):
const CACHE_VERSION = 'v2';
redis.get(`${CACHE_VERSION}:patient:uuid123`); // Returns v2 data

// Deployment:
1. Deploy new code with CACHE_VERSION = 'v2'
2. Old instances still use 'v1' prefix
3. New instances use 'v2' prefix
4. Both coexist (separate cache entries)
5. Old instances terminated → v1 keys naturally expire (TTL)

// Alternative: Flush cache on deployment (if acceptable downtime)
redis.flushAll(); // Use carefully
```

**7. API Versioning**

**Challenge**: Frontend and backend versions may mismatch

**Solution**: API versioning from day 1

```
API Structure:
/api/v1/patients
/api/v1/consultations
/api/v1/prescriptions

When breaking change needed:
/api/v2/prescriptions (new format)

Support both v1 and v2 simultaneously for 3 months
- v1: Deprecated but functional
- v2: New format

Frontend:
- Detects backend API version
- Uses appropriate client
- Graceful degradation if v2 not available
```

**8. Health Checks & Auto-Recovery**

```typescript
// Health check endpoint
app.get('/health', async (req, res) => {
  const checks = {
    database: await checkDatabase(),
    redis: await checkRedis(),
    openai: await checkOpenAI(),
    s3: await checkS3()
  };
  
  const isHealthy = Object.values(checks).every(c => c.healthy);
  
  if (isHealthy) {
    res.status(200).json({ status: 'healthy', checks });
  } else {
    res.status(503).json({ status: 'unhealthy', checks });
  }
});

// ECS task configuration
{
  "healthCheck": {
    "command": ["CMD-SHELL", "curl -f http://localhost:3000/health || exit 1"],
    "interval": 30,
    "timeout": 5,
    "retries": 3,
    "startPeriod": 60
  }
}

// Auto-recovery:
If health check fails 3 times → ECS kills task → Launches new task
```

**9. Monitoring & Alerting for Live Deployments**

**CloudWatch Alarms**:
```
Critical Alarms (PagerDuty):
1. API Error Rate > 5% for 5 minutes
2. Database Connection Failures
3. OpenAI API Success Rate < 90%
4. ECS Task Count < 2 (should be min 3)

Warning Alarms (Slack):
1. API Latency p99 > 3s for 10 minutes
2. Memory Usage > 80% for 15 minutes
3. Prescription Approval Rate < 80%
4. Order Payment Failures > 10%

Deployment-Specific Alarms:
During canary release:
- Canary error rate vs Stable error rate
- If canary > stable + 2%: Rollback
```

**Custom Metrics**:
```typescript
// Log custom business metrics
import { CloudWatch } from 'aws-sdk';
const cloudwatch = new CloudWatch();

const logMetric = (metricName, value) => {
  cloudwatch.putMetricData({
    Namespace: 'HealthcareApp',
    MetricData: [{
      MetricName: metricName,
      Value: value,
      Timestamp: new Date(),
      Unit: 'Count'
    }]
  });
};

// Usage
logMetric('ConsultationCompleted', 1);
logMetric('PrescriptionGenerated', 1);
logMetric('PaymentSuccess', 1);
```

**10. Incident Response Playbook**

```
If Deployment Goes Wrong:

Severity 1 (Site Down):
1. Immediate rollback (< 2 min)
2. Run: ./scripts/rollback.sh
3. Verify site recovery
4. Post-mortem within 24 hours

Severity 2 (Feature Broken):
1. Disable feature flag (< 1 min)
2. Investigate issue
3. Fix + re-deploy next day
4. Gradual re-enable

Severity 3 (Minor Bug):
1. Log issue
2. Monitor impact
3. Scheduled fix in next sprint
```

---

## DEPLOYMENT CHECKLIST (For Each Release)

**Pre-Deployment**:
- [ ] Code reviewed (2 approvals)
- [ ] All tests passing (unit + integration)
- [ ] Staging deployment successful
- [ ] Database migrations tested
- [ ] Feature flags configured
- [ ] Rollback plan documented
- [ ] On-call engineer assigned

**During Deployment**:
- [ ] Deploy to 1 canary instance
- [ ] Smoke tests pass on canary
- [ ] Monitor for 15 minutes
- [ ] Gradual rollout: 5% → 25% → 50% → 100%
- [ ] Monitor each stage for 15 minutes

**Post-Deployment**:
- [ ] All health checks green
- [ ] Error rate < 1%
- [ ] Latency within SLA
- [ ] Business metrics normal
- [ ] Monitor for 1 hour
- [ ] Document any issues

---

## FEATURE ROLLOUT CALENDAR (Day 46-120)

| Sprint | Week | Days | Feature | Deployment Strategy |
|--------|------|------|---------|---------------------|
| 1 | 10-11 | 46-55 | Lab Testing | Canary 5%→100% (5 days) |
| 2 | 12-13 | 56-65 | Family Accounts | Feature flag 10%→100% |
| 3 | 14-15 | 66-75 | QR Sharing | Feature flag 5%→100% |
| 4 | 16-17 | 76-85 | Identity Verification | Feature flag 1%→100% |
| 5 | 18-19 | 86-95 | Genetic Testing | Gated (identity required) |
| 6 | 20-21 | 96-105 | Data Analytics | Backend only (no UI) |
| 7 | 22-23 | 106-115 | Advertisements | A/B test 50/50 |
| 8 | 24 | 116-120 | Push Notifications | Opt-in rollout |

---

## SUCCESS METRICS (Tracked Live)

**Technical Metrics**:
- Deployment Frequency: Target 2x/week
- Mean Time to Recovery (MTTR): < 1 hour
- Change Failure Rate: < 5%
- Lead Time (code → production): < 24 hours

**Business Metrics**:
- Daily Active Users (DAU)
- Consultation Completion Rate: > 80%
- Prescription-to-Order Conversion: > 60%
- Payment Success Rate: > 95%
- Customer Satisfaction (NPS): > 50

**AI Performance**:
- AI Prescription Approval Rate: > 85%
- Average Consultation Time: < 10 minutes
- Emergency Detection Accuracy: 100%
- Multi-language Success Rate: > 90%

---

## CONCLUSION

**MVP Delivered (Day 45)**:
✓ Fully functional AI healthcare platform
✓ Consultation → Prescription → Purchase flow
✓ Physician review with eSign
✓ Basic payments + OTP-on-delivery
✓ 100 concurrent users supported

**Live Feature Rollout (Day 46-120)**:
✓ 8 major features added while live
✓ Zero downtime deployments
✓ Gradual rollouts with monitoring
✓ Instant rollback capability

**Key Success Factors**:
1. Microservices architecture (easy to add features)
2. Feature flags (controlled rollouts)
3. Comprehensive monitoring (catch issues early)
4. Blue-green deployments (zero downtime)
5. Database versioning (backward compatibility)
6. Automated rollbacks (safety net)

**Next Phase (Month 6+)**:
- Mobile app launch (React Native)
- White-label for clinics
- International expansion (UAE, SE Asia)
- Chronic disease management
- Insurance integration

---

This plan delivers a production-ready healthcare platform in 45 days, then continuously evolves with live feature rollouts using industry-best deployment practices.