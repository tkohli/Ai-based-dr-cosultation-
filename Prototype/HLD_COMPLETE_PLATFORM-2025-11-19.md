# High-Level Design: Complete AI Healthcare Platform
## India-First, Global-Ready Architecture

---

## Executive Summary

This document presents the technical architecture for a comprehensive AI-powered healthcare platform designed for the Indian market with global expansion capabilities. The platform integrates **AI-driven consultations, physician oversight, medicine e-commerce, lab testing, genetic testing, and advanced features** including family accounts, QR-based medical sharing, advertisements, and de-identified analytics.

**Core Innovation**: Combines AI efficiency with physician oversight, creating a hybrid model that delivers instant preliminary assessments while maintaining medical accuracy through licensed doctor review and digital signatures.

**Target Scale**: 10,000 daily consultations, 15,000 medicine orders, 3,000 lab bookings
**Geography**: India (MVP), UAE and Southeast Asia (Phase 2)
**Timeline**: 45-day MVP, continuous feature rollout

---

## System Architecture Overview

### Complete System Flow

```
Patient Entry
    ↓
AI Avatar Intake (Voice/Text)
    ↓
RAG Privacy Layer (PHI Stripping)
    ↓
LLM Processing (Med/Lab Suggestion)
    ↓
Prescription Draft Generated
    ↓
Physician Review Portal
    ↓
Physician e-Sign (Aadhaar)
    ↓
Patient Digital Signature
    ↓
Prescription Released
    ↓
┌────────────────┬─────────────────┬────────────────┐
│                │                 │                │
▼                ▼                 ▼                ▼
Pharmacy      Lab Booking     Genetic Test    Download
Selection      (Partners)      (Special)       Prescription
    ↓                ↓              ↓
Payment        Payment         Enhanced
(Wallet/UPI)   (Gateway)       Consent +
    ↓                ↓          Digital Sign
OTP-on-        Collection          ↓
Delivery       Scheduled       Payment
    ↓                ↓              ↓
Merchant       Report          Kit Delivery
Settlement     Upload              ↓
    ↓                ↓          Sample
Order          AI Report       Collection
Complete       Analysis            ↓
                   ↓           Report
              (Optional)       (Encrypted)
              Follow-up
```

### High-Level Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │  Patient   │  │  Physician │  │  Pharmacy  │  │  Lab/Admin │   │
│  │  Web/App   │  │  Dashboard │  │  Portal    │  │  Portal    │   │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘   │
└────────────┬─────────────────┬────────────────┬──────────────────────┘
             │                 │                │
             ▼                 ▼                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                                │
│  AWS API Gateway + CloudFront CDN                                     │
│  - Rate Limiting    - JWT Auth    - CORS    - Request Validation     │
└────────────┬─────────────────┬────────────────┬──────────────────────┘
             │                 │                │
             ▼                 ▼                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     CORE SERVICE LAYER                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ AI Avatar    │  │  RAG Privacy │  │ Consultation │              │
│  │ Service      │  │  Layer       │  │ Orchestrator │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Physician    │  │  Patient     │  │  Prescription│              │
│  │ Review Svc   │  │  Service     │  │  Service     │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└────────────┬─────────────────┬────────────────┬──────────────────────┘
             │                 │                │
             ▼                 ▼                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                   BUSINESS SERVICES LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  E-Commerce  │  │  Lab Booking │  │  Genetic     │              │
│  │  Service     │  │  Service     │  │  Testing Svc │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  Payment &   │  │  Family      │  │  QR Medical  │              │
│  │  Wallet Svc  │  │  Account Svc │  │  Share Svc   │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└────────────┬─────────────────┬────────────────┬──────────────────────┘
             │                 │                │
             ▼                 ▼                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    SHARED SERVICES LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  Auth &      │  │  Notification│  │  Document    │              │
│  │  Identity    │  │  Service     │  │  Management  │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  Analytics & │  │  Ad          │  │  Audit &     │              │
│  │  Aggregation │  │  Service     │  │  Logging     │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└────────────┬─────────────────┬────────────────┬──────────────────────┘
             │                 │                │
             ▼                 ▼                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  PostgreSQL  │  │   MongoDB    │  │   Redis      │              │
│  │  (Primary)   │  │  (Documents) │  │   (Cache)    │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  Pinecone    │  │   AWS S3     │  │  Redshift    │              │
│  │  (Vectors)   │  │  (Storage)   │  │  (Analytics) │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└────────────┬─────────────────┬────────────────┬──────────────────────┘
             │                 │                │
             ▼                 ▼                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL INTEGRATIONS                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  OpenAI      │  │  D-ID Avatar │  │  AWS AI      │              │
│  │  GPT-4       │  │  API         │  │  Services    │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  Razorpay    │  │  Aadhaar     │  │  MSG91 /     │              │
│  │  Payments    │  │  eSign       │  │  Twilio      │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  Lab Partner │  │  Pharmacy    │  │  Delivery    │              │
│  │  APIs        │  │  APIs        │  │  Partners    │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Core Module Specifications

### 1. AI Avatar Intake Module

**Purpose**: Intelligent conversational interface for patient symptom gathering

**Technology Stack**:
- **3D Avatar**: D-ID API / Synthesia
- **Speech-to-Text**: AWS Transcribe (real-time streaming)
- **Text-to-Speech**: AWS Polly (neural voices)
- **Real-time Communication**: WebRTC
- **Session Management**: Redis + WebSocket

**Features**:
- Animated 3D avatar with lip-sync
- Multi-language support (Hindi, English, Tamil, Telugu, Bengali, Marathi)
- Voice and text input modes
- Emotion detection (optional)
- Context-aware follow-up questions
- Medical terminology understanding

**Flow**:
```
1. Patient clicks "Start Consultation"
2. Avatar loads with greeting in preferred language
3. Patient speaks/types symptoms
4. Audio → AWS Transcribe → Text
5. Text → Anonymization Layer → RAG Context Retrieval
6. RAG Context + Text → OpenAI → Response
7. Response → AWS Polly → Speech
8. Speech → D-ID (lip-sync animation) → Avatar speaks
9. Loop continues until consultation complete
10. Avatar summarizes and generates prescription draft
```

**API Endpoints**:
```
POST   /api/v1/avatar/session/start
POST   /api/v1/avatar/message
GET    /api/v1/avatar/session/:sessionId
POST   /api/v1/avatar/session/:sessionId/complete
WebSocket: wss://api.domain.com/avatar/stream
```

**Data Models**:
```typescript
interface AvatarSession {
  id: string;
  patientId: string;
  language: string;
  mode: 'VOICE' | 'TEXT' | 'HYBRID';
  startedAt: Date;
  status: 'ACTIVE' | 'COMPLETED' | 'ABANDONED';
  conversationId: string;
}

interface AvatarMessage {
  sessionId: string;
  role: 'PATIENT' | 'AVATAR';
  content: string;
  audioUrl?: string;
  timestamp: Date;
  metadata: {
    transcriptionConfidence?: number;
    languageDetected?: string;
  };
}
```

---

### 2. RAG Privacy Layer

**Purpose**: Strip PHI before sending to LLM, retrieve relevant medical context

**Architecture**:
```
Patient Input → PHI Detection → Anonymization → Vector Search → Context Injection → LLM
                     ↓                                    ↓
              Blocked Terms DB              Medical Knowledge Base (Embedded)
```

**Components**:

**A. PHI Stripping Service**
```typescript
interface PHIStripper {
  stripPHI(text: string): AnonymizedText;
  detectPHI(text: string): PHIEntity[];
  tokenize(text: string, entities: PHIEntity[]): TokenizedText;
}

interface PHIEntity {
  type: 'NAME' | 'PHONE' | 'ADDRESS' | 'DOB' | 'ID_NUMBER';
  value: string;
  startIndex: number;
  endIndex: number;
  replacement: string; // TOKEN_001, TOKEN_002
}

// Example
Input: "My name is Rajesh Kumar, phone 9876543210, I have fever"
Output: {
  anonymized: "[NAME_TOKEN_1], I have fever",
  tokens: {
    NAME_TOKEN_1: { type: 'NAME', value: 'Rajesh Kumar' },
    PHONE_TOKEN_1: { type: 'PHONE', value: '9876543210' }
  }
}
```

**B. Vector Database (Pinecone)**
```typescript
// Medical Knowledge Base
interface MedicalDocument {
  id: string;
  type: 'CONDITION' | 'MEDICINE' | 'PROTOCOL' | 'INTERACTION';
  content: string;
  embedding: number[]; // 1536-dim vector (OpenAI ada-002)
  metadata: {
    condition?: string;
    medicines?: string[];
    severity?: string;
    language: string;
  };
}

// RAG Retrieval
async function retrieveContext(symptoms: string): Promise<string[]> {
  const embedding = await openai.embeddings.create({
    model: "text-embedding-ada-002",
    input: symptoms
  });
  
  const results = await pinecone.query({
    vector: embedding.data[0].embedding,
    topK: 5,
    includeMetadata: true
  });
  
  return results.matches.map(m => m.metadata.content);
}
```

**C. Prompt Construction**
```typescript
function buildPrompt(
  anonymizedSymptoms: string,
  ragContext: string[],
  conversationHistory: Message[]
): string {
  return `
You are a medical AI assistant conducting a patient consultation in India.

MEDICAL KNOWLEDGE BASE:
${ragContext.join('\n\n')}

CONVERSATION HISTORY:
${conversationHistory.map(m => `${m.role}: ${m.content}`).join('\n')}

PATIENT'S CURRENT MESSAGE:
${anonymizedSymptoms}

INSTRUCTIONS:
- Ask relevant follow-up questions
- Be empathetic and clear
- Use medical knowledge base for accuracy
- Do NOT prescribe controlled substances
- Flag emergency symptoms immediately

YOUR RESPONSE:
`;
}
```

**Security Measures**:
- All PHI encrypted at rest (AES-256)
- TLS 1.3 in transit
- Audit logs for all PHI access
- Anonymization logs immutable
- Regular pen testing

---

### 3. Medication & Lab Suggestion Engine

**Purpose**: Generate evidence-based medication and lab test recommendations

**Knowledge Base Structure**:
```
medicines_db (PostgreSQL)
  - id, name, generic_name, category, schedule
  - indications[], contraindications[]
  - dosage_forms[], standard_dosages
  - drug_interactions[], side_effects[]
  
treatment_protocols (MongoDB)
  - condition
  - first_line_medications[]
  - alternative_medications[]
  - contraindications[]
  - required_lab_tests[]
  - follow_up_recommendations

lab_tests_db (PostgreSQL)
  - id, name, category, description
  - indications[], preparation_required
  - normal_ranges, interpretation_guide
```

**Prescription Generation Logic**:
```typescript
interface PrescriptionDraft {
  diagnosis: string;
  diagnosisConfidence: 'HIGH' | 'MEDIUM' | 'LOW';
  medications: MedicationRecommendation[];
  labTests: LabTestRecommendation[];
  lifestyleAdvice: string[];
  redFlags: string[];
  followUpDays: number;
  aiReasoning: string;
}

async function generatePrescription(
  consultation: Consultation
): Promise<PrescriptionDraft> {
  // Extract structured data from conversation
  const extractedData = await extractMedicalInfo(consultation.messages);
  
  // Get treatment protocol from knowledge base
  const protocol = await getTreatmentProtocol(extractedData.symptoms);
  
  // Call OpenAI with structured prompt
  const prescription = await openai.chat.completions.create({
    model: "gpt-4",
    messages: [{
      role: "system",
      content: PRESCRIPTION_GENERATION_PROMPT
    }, {
      role: "user",
      content: JSON.stringify({
        symptoms: extractedData.symptoms,
        duration: extractedData.duration,
        severity: extractedData.severity,
        medicalHistory: extractedData.medicalHistory,
        currentMedications: extractedData.currentMedications,
        allergies: extractedData.allergies,
        protocol: protocol
      })
    }],
    response_format: { type: "json_object" }
  });
  
  const draft = JSON.parse(prescription.choices[0].message.content);
  
  // Safety validation
  await validatePrescriptionSafety(draft);
  
  return draft;
}
```

**Safety Validation**:
```typescript
async function validatePrescriptionSafety(
  draft: PrescriptionDraft
): Promise<ValidationResult> {
  const issues: string[] = [];
  
  // Check 1: Controlled substances
  for (const med of draft.medications) {
    if (CONTROLLED_SUBSTANCES.includes(med.genericName)) {
      throw new Error('AI cannot prescribe controlled substances');
    }
  }
  
  // Check 2: Drug interactions
  const interactions = await checkDrugInteractions(
    draft.medications.map(m => m.genericName)
  );
  if (interactions.severe.length > 0) {
    issues.push('Severe drug interactions detected');
  }
  
  // Check 3: Allergy conflicts
  const allergies = await getPatientAllergies(draft.patientId);
  for (const med of draft.medications) {
    if (allergies.includes(med.genericName)) {
      throw new Error('Prescription contains allergen');
    }
  }
  
  // Check 4: Dosage ranges
  for (const med of draft.medications) {
    const range = await getStandardDosageRange(med.genericName);
    if (!isWithinRange(med.dosage, range)) {
      issues.push(`Dosage out of range for ${med.name}`);
    }
  }
  
  return {
    isValid: issues.length === 0,
    issues: issues
  };
}
```

**Suggested Lab Tests**:
```typescript
async function recommendLabTests(
  symptoms: string[],
  diagnosis: string
): Promise<LabTestRecommendation[]> {
  // Rule-based + AI-based
  const ruleBasedTests = await getRuleBasedTests(diagnosis);
  
  const aiPrompt = `
    Given diagnosis: ${diagnosis}
    And symptoms: ${symptoms.join(', ')}
    
    Recommend relevant lab tests that would:
    1. Confirm diagnosis
    2. Rule out differential diagnoses
    3. Monitor treatment response
    
    Return as JSON array.
  `;
  
  const aiTests = await callOpenAI(aiPrompt);
  
  // Combine and deduplicate
  return [...new Set([...ruleBasedTests, ...aiTests])];
}
```

---

### 4. Physician Review Portal

**Purpose**: Licensed doctors review and approve/modify AI-generated prescriptions

**Dashboard Features**:
- Real-time queue of pending consultations
- Consultation detail view (full transcript + AI reasoning)
- Prescription edit interface
- Approve/Reject workflow
- Performance analytics

**User Interface**:
```
┌────────────────────────────────────────────────────────┐
│  Physician Dashboard                    Dr. Sharma  ↓  │
├────────────────────────────────────────────────────────┤
│  Pending Queue (23)        Completed (156)             │
│                                                         │
│  ┌──────────────────────────────────────────────────┐ │
│  │ URGENT (3)                                        │ │
│  │ ────────────────────────────────────────────────  │ │
│  │ Rajesh K. | Chest pain | 10 min ago      [REVIEW]│ │
│  │ Priya S.  | Severe headache | 15 min ago [REVIEW]│ │
│  └──────────────────────────────────────────────────┘ │
│                                                         │
│  ┌──────────────────────────────────────────────────┐ │
│  │ ROUTINE (20)                                      │ │
│  │ ────────────────────────────────────────────────  │ │
│  │ Amit P.   | Fever, cough | 2 min ago     [REVIEW]│ │
│  │ Sneha M.  | Acidity | 5 min ago          [REVIEW]│ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘

Consultation Detail View:
┌────────────────────────────────────────────────────────┐
│  Consultation #C123456              Status: PENDING     │
├────────────────────────────────────────────────────────┤
│  Patient: Amit P. (Age: 35, Male)                      │
│  Started: 2025-01-15 10:30 AM                          │
│                                                         │
│  TRANSCRIPT:                                            │
│  ────────────────────────────────────────────────────  │
│  Avatar: Hello! How can I help you today?              │
│  Patient: I have fever since 3 days with body ache     │
│  Avatar: What is your temperature?                     │
│  Patient: 101°F                                         │
│  ... (full conversation)                                │
│                                                         │
│  AI-GENERATED PRESCRIPTION:                             │
│  ────────────────────────────────────────────────────  │
│  Diagnosis: Viral Fever                                │
│  Confidence: HIGH                                       │
│                                                         │
│  Medications:                                           │
│  1. Paracetamol 500mg - TDS x 5 days                   │
│  2. Cetirizine 10mg - OD x 3 days (if needed)          │
│                                                         │
│  [EDIT] [APPROVE] [REJECT]                             │
└────────────────────────────────────────────────────────┘
```

**APIs**:
```
GET    /api/v1/physician/queue
GET    /api/v1/physician/consultation/:id
PUT    /api/v1/physician/prescription/:id/edit
POST   /api/v1/physician/prescription/:id/approve
POST   /api/v1/physician/prescription/:id/reject
```

**Approval Flow**:
```typescript
async function approvePrescription(
  prescriptionId: string,
  physicianId: string,
  modifications?: PrescriptionModifications
): Promise<void> {
  // 1. Update prescription
  if (modifications) {
    await updatePrescription(prescriptionId, modifications);
  }
  
  // 2. Generate PDF
  const pdfUrl = await generatePrescriptionPDF(prescriptionId);
  
  // 3. Trigger Aadhaar eSign
  const signatureRequest = await initiateAadhaarESign({
    physicianId: physicianId,
    documentUrl: pdfUrl,
    purpose: 'Medical Prescription Approval'
  });
  
  // 4. Wait for OTP entry and signature
  // (Webhook callback from eSign provider)
  
  // 5. Once signed, update status
  await updatePrescriptionStatus(prescriptionId, 'APPROVED');
  
  // 6. Notify patient
  await notifyPatient(prescriptionId, 'prescription_ready');
}
```

---

### 5. Aadhaar eSign Integration

**Purpose**: Legally valid digital signature for prescriptions

**Provider Options**:
- e-Mudhra
- NSDL e-Gov
- eMudhra Digital Signature Gateway

**Integration Flow**:
```
1. Physician clicks "Approve with eSign"
2. Backend calls eSign API with document
3. eSign provider sends OTP to physician's Aadhaar-linked mobile
4. Physician enters OTP in portal
5. eSign provider validates with UIDAI
6. Digital certificate applied to PDF
7. Signed PDF returned to backend
8. Verification hash stored in database
9. Prescription marked as APPROVED
```

**API Integration**:
```typescript
interface ESignProvider {
  initiateSignature(request: SignatureRequest): Promise<SignatureSession>;
  verifyOTP(sessionId: string, otp: string): Promise<SignedDocument>;
  verifySignature(documentHash: string): Promise<boolean>;
}

class EMudhraAdapter implements ESignProvider {
  async initiateSignature(request: SignatureRequest) {
    const response = await axios.post('https://emudhra.com/api/sign/initiate', {
      document_url: request.documentUrl,
      signer_aadhaar_last4: request.physicianAadhaar,
      purpose: request.purpose
    }, {
      headers: { 'Authorization': `Bearer ${EMUDHRA_API_KEY}` }
    });
    
    return {
      sessionId: response.data.session_id,
      expiresAt: response.data.expires_at
    };
  }
  
  async verifyOTP(sessionId: string, otp: string) {
    const response = await axios.post('https://emudhra.com/api/sign/verify', {
      session_id: sessionId,
      otp: otp
    });
    
    return {
      signedDocumentUrl: response.data.signed_document_url,
      signatureHash: response.data.signature_hash,
      certificateDetails: response.data.certificate
    };
  }
}
```

**Database Storage**:
```sql
CREATE TABLE digital_signatures (
  id UUID PRIMARY KEY,
  prescription_id UUID REFERENCES prescriptions(id),
  physician_id UUID REFERENCES physicians(id),
  signature_hash VARCHAR(64) NOT NULL,
  certificate_details JSONB NOT NULL,
  signed_document_url TEXT NOT NULL,
  provider VARCHAR(50) NOT NULL,
  signed_at TIMESTAMP NOT NULL,
  aadhaar_last4 VARCHAR(4),
  is_valid BOOLEAN DEFAULT TRUE
);
```

---

### 6. Patient Digital Signature Module (NEW)

**Purpose**: Capture patient consent and acknowledgment before prescription release

**Trigger Points**:
1. Before viewing final approved prescription
2. Before consenting to genetic testing
3. Before sharing medical records via QR
4. For telemedicine consent forms

**Implementation**:

**Frontend Component**:
```typescript
import SignatureCanvas from 'react-signature-canvas';

const PatientSignatureModal = ({ prescriptionId, onComplete }) => {
  const sigPad = useRef<SignatureCanvas>(null);
  
  const handleSubmit = async () => {
    if (sigPad.current.isEmpty()) {
      alert('Please provide signature');
      return;
    }
    
    const signatureDataURL = sigPad.current.toDataURL('image/png');
    
    await api.submitPatientSignature({
      prescriptionId,
      signatureData: signatureDataURL,
      timestamp: new Date().toISOString(),
      ipAddress: await getUserIP(),
      deviceInfo: navigator.userAgent,
      consent: true
    });
    
    onComplete();
  };
  
  return (
    <Modal>
      <h2>Prescription Consent</h2>
      <p>Please review and sign to acknowledge you have received 
         and understood your prescription.</p>
      
      <SignatureCanvas
        ref={sigPad}
        canvasProps={{
          width: 500,
          height: 200,
          className: 'signature-canvas'
        }}
      />
      
      <Button onClick={() => sigPad.current.clear()}>Clear</Button>
      <Button onClick={handleSubmit}>Submit & View Prescription</Button>
    </Modal>
  );
};
```

**Backend Service**:
```typescript
interface PatientSignatureService {
  captureSignature(data: SignatureData): Promise<Signature>;
  verifySignature(signatureId: string): Promise<boolean>;
  getSignature(prescriptionId: string): Promise<Signature>;
}

async function captureSignature(data: SignatureData) {
  // 1. Upload signature image to S3
  const s3Key = `signatures/patient/${data.prescriptionId}.png`;
  await s3.upload({
    Key: s3Key,
    Body: Buffer.from(data.signatureData.split(',')[1], 'base64'),
    ContentType: 'image/png'
  });
  
  // 2. Generate signature hash
  const signatureHash = crypto
    .createHash('sha256')
    .update(data.signatureData)
    .digest('hex');
  
  // 3. Store metadata
  const signature = await db.patient_signatures.create({
    id: uuid(),
    prescription_id: data.prescriptionId,
    patient_id: data.patientId,
    signature_url: `https://cdn.domain.com/${s3Key}`,
    signature_hash: signatureHash,
    ip_address: data.ipAddress,
    device_info: data.deviceInfo,
    timestamp: new Date(),
    is_valid: true
  });
  
  // 4. Create immutable audit log
  await auditLog.create({
    event: 'PATIENT_SIGNATURE_CAPTURED',
    entity_type: 'PRESCRIPTION',
    entity_id: data.prescriptionId,
    actor_id: data.patientId,
    metadata: {
      signature_id: signature.id,
      signature_hash: signatureHash
    }
  });
  
  // 5. Update prescription status
  await db.prescriptions.update({
    id: data.prescriptionId,
    patient_signature_id: signature.id,
    patient_acknowledged_at: new Date()
  });
  
  return signature;
}
```

**Database Schema**:
```sql
CREATE TABLE patient_signatures (
  id UUID PRIMARY KEY,
  prescription_id UUID REFERENCES prescriptions(id),
  patient_id UUID REFERENCES patients(id),
  signature_url TEXT NOT NULL,
  signature_hash VARCHAR(64) UNIQUE NOT NULL,
  ip_address INET NOT NULL,
  device_info TEXT,
  timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
  consent_text TEXT,
  is_valid BOOLEAN DEFAULT TRUE,
  revoked_at TIMESTAMP,
  revocation_reason TEXT
);

CREATE INDEX idx_patient_sig_prescription 
  ON patient_signatures(prescription_id);
CREATE INDEX idx_patient_sig_patient 
  ON patient_signatures(patient_id);
```

**Consent Text** (displayed before signing):
```
PATIENT CONSENT AND ACKNOWLEDGMENT

I acknowledge that:
1. I have received medical consultation via AI-assisted platform
2. The prescription has been reviewed and approved by a licensed physician
3. I have read and understood the prescribed medications, dosages, and instructions
4. I have disclosed all relevant medical history, allergies, and current medications
5. I will follow the prescription as directed
6. I will seek immediate medical attention if symptoms worsen
7. This is not a substitute for emergency medical care

By signing below, I consent to the above and confirm receipt of my prescription.

Signature: _________________    Date: ___________
```

---

### 7. Pharmacy & Lab Marketplace

**Pharmacy Module**:

**Features**:
- Medicine catalog with search and filters
- Prescription-to-cart automatic conversion
- Generic alternative suggestions
- Multi-warehouse inventory management
- Real-time stock checking
- Order tracking
- Merchant portal

**Medicine Catalog API**:
```typescript
interface MedicineCatalog {
  searchMedicines(query: string, filters: SearchFilters): Promise<Medicine[]>;
  getMedicineById(id: string): Promise<Medicine>;
  getAlternatives(medicineId: string): Promise<Medicine[]>;
  checkAvailability(medicineId: string, pincode: string): Promise<InventoryStatus>;
}

interface Medicine {
  id: string;
  name: string;
  genericName: string;
  manufacturer: string;
  category: string;
  form: 'Tablet' | 'Capsule' | 'Syrup' | 'Injection' | 'Cream';
  strength: string;
  packSize: string;
  mrp: number;
  sellingPrice: number;
  discountPercent: number;
  prescriptionRequired: boolean;
  schedule: 'H' | 'H1' | 'X' | 'OTC';
  images: string[];
  description: string;
  uses: string[];
  sideEffects: string[];
  contraindications: string[];
  storageConditions: string;
  manufacturer: string;
  countryOfOrigin: string;
}
```

**Prescription-to-Cart Conversion**:
```typescript
async function createOrderFromPrescription(
  prescriptionId: string,
  patientId: string
): Promise<Cart> {
  const prescription = await getPrescription(prescriptionId);
  const patient = await getPatient(patientId);
  
  const cart: Cart = {
    items: [],
    subtotal: 0,
    discount: 0,
    deliveryCharge: 0,
    total: 0
  };
  
  for (const prescribedMed of prescription.medications) {
    // Find exact match in catalog
    let medicine = await findMedicineByName(prescribedMed.medicineName);
    
    if (!medicine) {
      // Find by generic name
      medicine = await findMedicineByGeneric(prescribedMed.genericName);
    }
    
    if (medicine) {
      // Check availability in patient's area
      const availability = await checkInventory(
        medicine.id,
        prescribedMed.quantity,
        patient.pincode
      );
      
      if (availability.available) {
        cart.items.push({
          medicineId: medicine.id,
          name: medicine.name,
          quantity: prescribedMed.quantity,
          price: medicine.sellingPrice,
          total: medicine.sellingPrice * prescribedMed.quantity,
          warehouseId: availability.warehouseId
        });
      } else {
        // Suggest alternatives
        const alternatives = await getAlternatives(medicine.id);
        cart.items.push({
          prescribedMedicine: prescribedMed,
          status: 'OUT_OF_STOCK',
          alternatives: alternatives
        });
      }
    } else {
      cart.items.push({
        prescribedMedicine: prescribedMed,
        status: 'NOT_FOUND_IN_CATALOG'
      });
    }
  }
  
  // Calculate totals
  cart.subtotal = cart.items.reduce((sum, item) => sum + (item.total || 0), 0);
  cart.deliveryCharge = calculateDeliveryCharge(patient.pincode, cart.subtotal);
  cart.total = cart.subtotal + cart.deliveryCharge;
  
  return cart;
}
```

**Lab Booking Module**:

**Features**:
- Lab test catalog with descriptions
- Partner lab network integration
- Home sample collection scheduling
- Test booking with payment
- Report upload and management
- AI-powered report analysis

**Lab Partner Integration**:
```typescript
interface LabPartnerAPI {
  searchTests(query: string): Promise<LabTest[]>;
  checkAvailability(testIds: string[], pincode: string): Promise<Availability>;
  createBooking(booking: BookingRequest): Promise<BookingConfirmation>;
  getAvailableSlots(pincode: string, date: Date): Promise<TimeSlot[]>;
  getReportStatus(bookingId: string): Promise<ReportStatus>;
  downloadReport(bookingId: string): Promise<Buffer>;
}

// Example: Thyrocare Integration
class ThyrocareAdapter implements LabPartnerAPI {
  async createBooking(booking: BookingRequest) {
    const response = await axios.post(
      'https://velso.thyrocare.cloud/api/OrderMaster/createOrder',
      {
        api_key: THYROCARE_API_KEY,
        mobile: booking.patient.mobile,
        email: booking.patient.email,
        product: booking.tests.map(t => t.code).join(','),
        address: booking.address,
        pincode: booking.pincode,
        service_type: booking.homeCollection ? 'H' : 'L',
        appointment_date: booking.preferredDate,
        appointment_time: booking.preferredSlot
      }
    );
    
    return {
      bookingId: response.data.lead_id,
      partnerBookingId: response.data.order_id,
      status: 'CONFIRMED',
      amount: response.data.amount,
      collectionSlot: response.data.appointment_datetime
    };
  }
}
```

---

### 8. Payment & Wallet System

**Payment Gateway Integration (Razorpay)**:

**Supported Methods**:
- UPI (PhonePe, GPay, Paytm, etc.)
- Credit/Debit Cards
- Net Banking
- Wallets (Paytm, PhonePe, Amazon Pay)
- EMI options
- Gift Cards

**Payment Flow**:
```typescript
interface PaymentService {
  createPaymentIntent(order: Order): Promise<PaymentIntent>;
  processPayment(paymentId: string): Promise<PaymentResult>;
  verifyPayment(razorpaySignature: string): Promise<boolean>;
  refundPayment(paymentId: string, amount: number): Promise<RefundResult>;
}

async function createPaymentIntent(order: Order) {
  // Create Razorpay order
  const razorpayOrder = await razorpay.orders.create({
    amount: order.total * 100, // paise
    currency: 'INR',
    receipt: order.orderNumber,
    notes: {
      order_id: order.id,
      patient_id: order.patientId,
      order_type: order.type // MEDICINE, LAB, CONSULTATION
    }
  });
  
  // Store in database
  const payment = await db.payments.create({
    id: uuid(),
    order_id: order.id,
    patient_id: order.patientId,
    amount: order.total,
    razorpay_order_id: razorpayOrder.id,
    status: 'CREATED',
    created_at: new Date()
  });
  
  return {
    paymentId: payment.id,
    razorpayOrderId: razorpayOrder.id,
    amount: order.total,
    currency: 'INR',
    razorpayKeyId: RAZORPAY_KEY_ID
  };
}

// Frontend integration
const options = {
  key: razorpayKeyId,
  amount: amount * 100,
  currency: 'INR',
  name: 'HealthCare Platform',
  description: 'Medicine Order Payment',
  order_id: razorpayOrderId,
  handler: async (response) => {
    await verifyPayment({
      razorpay_order_id: response.razorpay_order_id,
      razorpay_payment_id: response.razorpay_payment_id,
      razorpay_signature: response.razorpay_signature
    });
  },
  prefill: {
    name: patient.name,
    email: patient.email,
    contact: patient.mobile
  },
  theme: {
    color: '#3399cc'
  }
};

const rzp = new Razorpay(options);
rzp.open();
```

**Wallet System**:

**Features**:
- Add money to wallet (Razorpay)
- Pay using wallet balance
- Wallet-to-wallet transfers (family accounts)
- Transaction history
- Auto-refill on low balance
- Gift card redemption

**Database Schema**:
```sql
CREATE TABLE wallets (
  id UUID PRIMARY KEY,
  patient_id UUID REFERENCES patients(id) UNIQUE,
  balance DECIMAL(10,2) DEFAULT 0.00,
  currency VARCHAR(3) DEFAULT 'INR',
  status VARCHAR(20) DEFAULT 'ACTIVE',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  CONSTRAINT positive_balance CHECK (balance >= 0)
);

CREATE TABLE wallet_transactions (
  id UUID PRIMARY KEY,
  wallet_id UUID REFERENCES wallets(id),
  type VARCHAR(20) NOT NULL, -- CREDIT, DEBIT
  amount DECIMAL(10,2) NOT NULL,
  balance_before DECIMAL(10,2) NOT NULL,
  balance_after DECIMAL(10,2) NOT NULL,
  reference_type VARCHAR(50), -- ORDER, REFUND, TOP_UP, GIFT_CARD
  reference_id UUID,
  description TEXT,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_wallet (wallet_id),
  INDEX idx_created (created_at DESC)
);
```

**Wallet Operations**:
```typescript
interface WalletService {
  getBalance(patientId: string): Promise<number>;
  addMoney(patientId: string, amount: number, paymentId: string): Promise<void>;
  deductMoney(patientId: string, amount: number, orderId: string): Promise<void>;
  getTransactionHistory(patientId: string): Promise<Transaction[]>;
  transfer(fromPatientId: string, toPatientId: string, amount: number): Promise<void>;
}

async function deductMoney(patientId: string, amount: number, orderId: string) {
  return await db.transaction(async (trx) => {
    // Lock wallet row
    const wallet = await trx('wallets')
      .where({ patient_id: patientId })
      .forUpdate()
      .first();
    
    if (!wallet) {
      throw new Error('Wallet not found');
    }
    
    if (wallet.balance < amount) {
      throw new Error('Insufficient balance');
    }
    
    const newBalance = wallet.balance - amount;
    
    // Update wallet
    await trx('wallets')
      .where({ id: wallet.id })
      .update({
        balance: newBalance,
        updated_at: new Date()
      });
    
    // Create transaction record
    await trx('wallet_transactions').insert({
      id: uuid(),
      wallet_id: wallet.id,
      type: 'DEBIT',
      amount: amount,
      balance_before: wallet.balance,
      balance_after: newBalance,
      reference_type: 'ORDER',
      reference_id: orderId,
      description: `Payment for order ${orderId}`,
      created_at: new Date()
    });
  });
}
```

**PPI Compliance**:
```
Note: Wallet system requires PPI (Prepaid Payment Instrument) license from RBI.

Options:
1. Apply for PPI license (12-18 months process)
2. Partner with licensed PPI provider (Paytm, PhonePe)
   - Use their wallet APIs
   - Revenue sharing model
3. Limit wallet to refunds only (no top-ups) - Doesn't require license

MVP Recommendation: Partner with Paytm/PhonePe for wallet functionality
```

---

### 9. OTP-on-Delivery Payment Release

**Purpose**: Ensure payment is released to merchant only after successful delivery

**Flow**:
```
1. Order placed and paid (amount held in escrow)
2. Medicine packed and shipped
3. Delivery partner reaches customer
4. System generates 6-digit OTP
5. OTP sent to customer's mobile
6. Delivery partner asks customer for OTP
7. Customer provides OTP verbally
8. Delivery partner enters OTP in app
9. Server verifies OTP
10. If valid:
    - Mark order as DELIVERED
    - Release payment to merchant
    - Send delivery confirmation to customer
11. If invalid:
    - Allow 2 more attempts
    - After 3 failures, escalate to support
```

**Implementation**:
```typescript
interface OTPService {
  generateOTP(orderId: string): Promise<OTP>;
  verifyOTP(orderId: string, otp: string): Promise<boolean>;
  resendOTP(orderId: string): Promise<void>;
}

async function generateOTP(orderId: string): Promise<OTP> {
  // Generate 6-digit OTP
  const otpCode = Math.floor(100000 + Math.random() * 900000).toString();
  
  // Store in Redis with 10-minute expiry
  await redis.setex(
    `otp:order:${orderId}`,
    600, // 10 minutes
    JSON.stringify({
      code: otpCode,
      attempts: 0,
      generated_at: new Date()
    })
  );
  
  // Send SMS
  await smsService.send({
    to: order.patient.mobile,
    message: `Your OTP for order ${order.orderNumber} delivery is: ${otpCode}. Valid for 10 minutes.`
  });
  
  return { code: otpCode, expiresAt: Date.now() + 600000 };
}

async function verifyOTP(orderId: string, otp: string): Promise<boolean> {
  const key = `otp:order:${orderId}`;
  const storedOTP = await redis.get(key);
  
  if (!storedOTP) {
    throw new Error('OTP expired or not found');
  }
  
  const otpData = JSON.parse(storedOTP);
  
  if (otpData.attempts >= 3) {
    throw new Error('Maximum OTP attempts exceeded');
  }
  
  otpData.attempts++;
  await redis.setex(key, 600, JSON.stringify(otpData));
  
  if (otpData.code === otp) {
    // OTP verified
    await redis.del(key);
    
    // Release payment to merchant
    await releasePaymentToMerchant(orderId);
    
    // Update order status
    await db.orders.update({
      id: orderId,
      status: 'DELIVERED',
      delivered_at: new Date(),
      otp_verified_at: new Date()
    });
    
    return true;
  }
  
  return false;
}

async function releasePaymentToMerchant(orderId: string) {
  const order = await getOrder(orderId);
  
  // Calculate merchant payout (order total - platform commission)
  const platformCommission = order.total * 0.05; // 5%
  const merchantPayout = order.total - platformCommission;
  
  // Create payout to merchant bank account
  await razorpay.payouts.create({
    account_number: RAZORPAY_ACCOUNT_NUMBER,
    amount: merchantPayout * 100,
    currency: 'INR',
    mode: 'IMPS',
    purpose: 'payout',
    fund_account_id: order.merchant.fundAccountId,
    queue_if_low_balance: true,
    reference_id: order.id,
    narration: `Payment for order ${order.orderNumber}`
  });
  
  // Update merchant ledger
  await db.merchant_transactions.create({
    merchant_id: order.merchant.id,
    order_id: order.id,
    type: 'CREDIT',
    amount: merchantPayout,
    commission: platformCommission,
    status: 'PROCESSING',
    created_at: new Date()
  });
}
```

**Delivery Partner App Mock**:
```typescript
// Delivery partner mobile app
const DeliveryConfirmation = ({ orderId }) => {
  const [otp, setOTP] = useState('');
  const [attempts, setAttempts] = useState(0);
  
  const handleVerify = async () => {
    try {
      const result = await api.verifyDeliveryOTP(orderId, otp);
      
      if (result.verified) {
        alert('Delivery confirmed! Payment released.');
        navigation.navigate('NextDelivery');
      } else {
        setAttempts(attempts + 1);
        alert(`Invalid OTP. ${3 - attempts} attempts remaining.`);
      }
    } catch (error) {
      alert(error.message);
    }
  };
  
  return (
    <View>
      <Text>Order #{orderNumber}</Text>
      <Text>Ask customer for OTP</Text>
      <TextInput
        value={otp}
        onChangeText={setOTP}
        keyboardType="numeric"
        maxLength={6}
        placeholder="Enter 6-digit OTP"
      />
      <Button title="Verify & Complete Delivery" onPress={handleVerify} />
    </View>
  );
};
```

---

### 10. Multi-Role User Management

**Roles**:
1. **Super Admin** - Full system access
2. **Patient** - Consultation, orders, family management
3. **Physician** - Review prescriptions, manage profile
4. **Pharmacy Merchant** - Order management, inventory
5. **Lab Partner** - Booking management, report upload
6. **Clinic Admin** - White-label clinic management
7. **Support Agent** - Customer support, issue resolution

**Authentication**:
- AWS Cognito User Pools (separate pools per role)
- JWT tokens with role-based claims
- OTP-based login for patients
- Email/Password for physicians and merchants
- MFA for admin roles

**Role-Based Access Control (RBAC)**:
```typescript
interface User {
  id: string;
  role: UserRole;
  permissions: Permission[];
  status: 'ACTIVE' | 'SUSPENDED' | 'DELETED';
}

enum UserRole {
  SUPER_ADMIN = 'SUPER_ADMIN',
  PATIENT = 'PATIENT',
  PHYSICIAN = 'PHYSICIAN',
  PHARMACY = 'PHARMACY',
  LAB_PARTNER = 'LAB_PARTNER',
  CLINIC_ADMIN = 'CLINIC_ADMIN',
  SUPPORT_AGENT = 'SUPPORT_AGENT'
}

enum Permission {
  // Patient permissions
  VIEW_OWN_CONSULTATIONS = 'view_own_consultations',
  CREATE_CONSULTATION = 'create_consultation',
  VIEW_OWN_PRESCRIPTIONS = 'view_own_prescriptions',
  PLACE_ORDER = 'place_order',
  MANAGE_FAMILY = 'manage_family',
  
  // Physician permissions
  VIEW_PENDING_CONSULTATIONS = 'view_pending_consultations',
  APPROVE_PRESCRIPTIONS = 'approve_prescriptions',
  REJECT_PRESCRIPTIONS = 'reject_prescriptions',
  
  // Pharmacy permissions
  VIEW_ORDERS = 'view_orders',
  UPDATE_ORDER_STATUS = 'update_order_status',
  MANAGE_INVENTORY = 'manage_inventory',
  
  // Admin permissions
  VIEW_ALL_USERS = 'view_all_users',
  MANAGE_USERS = 'manage_users',
  VIEW_ANALYTICS = 'view_analytics',
  MANAGE_SYSTEM_CONFIG = 'manage_system_config'
}

// Permission middleware
function requirePermissions(...requiredPermissions: Permission[]) {
  return async (req, res, next) => {
    const user = req.user;
    
    const hasPermission = requiredPermissions.every(p => 
      user.permissions.includes(p)
    );
    
    if (!hasPermission) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    
    next();
  };
}

// Usage
router.get('/prescriptions/pending',
  authenticate,
  requirePermissions(Permission.VIEW_PENDING_CONSULTATIONS),
  getPendingPrescriptions
);
```

---

### 11. Family Accounts

**Purpose**: Allow patients to manage healthcare for family members

**Features**:
- Link multiple family members under one account
- Delegated access levels (Owner, Manager, Viewer)
- Consent tracking
- Separate medical histories
- Shared payment methods (optional)

**Access Levels**:
```
OWNER (Account Holder):
- Full access to own and all linked members' data
- Can add/remove family members
- Can set access levels for others
- Can initiate consultations for anyone
- Can view all prescriptions and orders

MANAGER (e.g., spouse):
- Can initiate consultations for linked members
- Can view medical history
- Can place orders
- Cannot remove family members

VIEWER (e.g., adult child checking on elderly parent):
- Can view medical history (read-only)
- Can view prescriptions and reports
- Cannot initiate consultations
- Cannot place orders
```

**Database Schema**:
```sql
CREATE TABLE family_accounts (
  id UUID PRIMARY KEY,
  owner_id UUID REFERENCES patients(id),
  member_id UUID REFERENCES patients(id),
  relationship VARCHAR(50), -- 'SPOUSE', 'CHILD', 'PARENT', 'SIBLING'
  access_level VARCHAR(20), -- 'OWNER', 'MANAGER', 'VIEWER'
  consent_given_at TIMESTAMP NOT NULL,
  consent_ip INET,
  added_by UUID REFERENCES patients(id),
  created_at TIMESTAMP DEFAULT NOW(),
  removed_at TIMESTAMP,
  
  UNIQUE(owner_id, member_id),
  CHECK (owner_id != member_id)
);

CREATE TABLE family_invites (
  id UUID PRIMARY KEY,
  inviter_id UUID REFERENCES patients(id),
  invitee_phone VARCHAR(15) NOT NULL,
  invitee_email VARCHAR(255),
  relationship VARCHAR(50),
  access_level VARCHAR(20),
  invite_code VARCHAR(10) UNIQUE NOT NULL,
  status VARCHAR(20) DEFAULT 'PENDING', -- PENDING, ACCEPTED, EXPIRED, REJECTED
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  accepted_at TIMESTAMP
);
```

**Invitation Flow**:
```typescript
async function inviteFamilyMember(request: FamilyInviteRequest) {
  // 1. Generate unique invite code
  const inviteCode = generateRandomCode(8);
  
  // 2. Create invite record
  const invite = await db.family_invites.create({
    id: uuid(),
    inviter_id: request.inviterId,
    invitee_phone: request.phone,
    invitee_email: request.email,
    relationship: request.relationship,
    access_level: request.accessLevel,
    invite_code: inviteCode,
    status: 'PENDING',
    expires_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days
    created_at: new Date()
  });
  
  // 3. Send invite via SMS and email
  const inviteLink = `https://app.healthcare.com/family/accept/${inviteCode}`;
  
  await smsService.send({
    to: request.phone,
    message: `${request.inviterName} has invited you to join their family account on HealthCare App. Click: ${inviteLink}`
  });
  
  if (request.email) {
    await emailService.send({
      to: request.email,
      subject: 'Family Account Invitation',
      html: renderFamilyInviteEmail(request.inviterName, inviteLink)
    });
  }
  
  return invite;
}

async function acceptFamilyInvite(inviteCode: string, acceptorId: string) {
  // 1. Verify invite
  const invite = await db.family_invites
    .findOne({ invite_code: inviteCode, status: 'PENDING' });
  
  if (!invite) {
    throw new Error('Invalid or expired invite');
  }
  
  if (new Date() > invite.expires_at) {
    throw new Error('Invite has expired');
  }
  
  // 2. Link family member
  await db.family_accounts.create({
    id: uuid(),
    owner_id: invite.inviter_id,
    member_id: acceptorId,
    relationship: invite.relationship,
    access_level: invite.access_level,
    consent_given_at: new Date(),
    added_by: invite.inviter_id,
    created_at: new Date()
  });
  
  // 3. Update invite status
  await db.family_invites.update({
    id: invite.id,
    status: 'ACCEPTED',
    accepted_at: new Date()
  });
  
  // 4. Notify inviter
  await notificationService.send({
    userId: invite.inviter_id,
    title: 'Family Member Added',
    body: `${acceptorName} has accepted your family account invitation.`
  });
}
```

---

### 12. QR-Based Medical Sharing

**Purpose**: Securely share medical records with other healthcare providers

**Features**:
- Generate time-limited QR codes
- Select specific records to share (prescriptions, reports, history)
- OTP-based access verification
- Audit trail of all access
- Revoke access anytime

**Flow**:
```
1. Patient selects records to share
2. System generates encrypted JWT token
3. JWT contains: record IDs, expiry, scope
4. JWT encoded in QR code
5. Recipient scans QR code
6. System shows "Enter OTP" screen
7. OTP sent to patient's mobile
8. Patient shares OTP with recipient verbally
9. Recipient enters OTP
10. If valid: Show medical records (read-only)
11. Access logged in audit trail
12. QR expires after 1 hour or manual revocation
```

**Implementation**:
```typescript
interface MedicalShareService {
  generateShareQR(request: ShareRequest): Promise<ShareQR>;
  validateShareToken(token: string): Promise<ShareTokenData>;
  verifyShareOTP(token: string, otp: string): Promise<ShareAccess>;
  revokeShareAccess(shareId: string): Promise<void>;
  getShareAuditLog(patientId: string): Promise<ShareLog[]>;
}

async function generateShareQR(request: ShareRequest) {
  // 1. Create share token
  const shareToken = jwt.sign(
    {
      patientId: request.patientId,
      recordIds: request.recordIds,
      recordTypes: request.recordTypes, // ['PRESCRIPTIONS', 'LAB_REPORTS']
      scope: 'medical_share',
      shareId: uuid(),
      exp: Math.floor(Date.now() / 1000) + (60 * 60) // 1 hour
    },
    JWT_SECRET,
    { algorithm: 'HS256' }
  );
  
  // 2. Store share metadata
  await db.medical_shares.create({
    id: shareToken.shareId,
    patient_id: request.patientId,
    record_ids: request.recordIds,
    record_types: request.recordTypes,
    token_hash: crypto.createHash('sha256').update(shareToken).digest('hex'),
    status: 'ACTIVE',
    expires_at: new Date(Date.now() + 60 * 60 * 1000),
    created_at: new Date()
  });
  
  // 3. Generate QR code data
  const qrData = JSON.stringify({
    type: 'MEDICAL_SHARE',
    token: shareToken,
    appUrl: 'https://app.healthcare.com/share/view',
    version: '1.0'
  });
  
  // 4. Generate QR code image
  const qrCodeImage = await QRCode.toDataURL(qrData, {
    width: 300,
    margin: 2,
    color: {
      dark: '#000000',
      light: '#FFFFFF'
    }
  });
  
  return {
    shareId: shareToken.shareId,
    qrCodeImage: qrCodeImage,
    qrData: qrData,
    expiresAt: new Date(Date.now() + 60 * 60 * 1000)
  };
}

async function validateShareToken(token: string) {
  try {
    // Verify JWT
    const decoded = jwt.verify(token, JWT_SECRET);
    
    // Check if share is still active
    const share = await db.medical_shares.findOne({
      id: decoded.shareId,
      status: 'ACTIVE'
    });
    
    if (!share) {
      throw new Error('Share has been revoked');
    }
    
    if (new Date() > share.expires_at) {
      throw new Error('Share has expired');
    }
    
    // Generate OTP
    const otp = Math.floor(100000 + Math.random() * 900000).toString();
    
    // Store OTP in Redis (5 minutes)
    await redis.setex(
      `share_otp:${decoded.shareId}`,
      300,
      JSON.stringify({ otp: otp, attempts: 0 })
    );
    
    // Send OTP to patient
    const patient = await getPatient(decoded.patientId);
    await smsService.send({
      to: patient.mobile,
      message: `Someone is requesting access to your medical records. OTP: ${otp}. Valid for 5 minutes. Do not share if you didn't initiate this.`
    });
    
    return {
      shareId: decoded.shareId,
      patientName: patient.name, // Redacted - "Rajesh K."
      recordTypes: decoded.recordTypes,
      requiresOTP: true
    };
    
  } catch (error) {
    throw new Error('Invalid or expired share token');
  }
}

async function verifyShareOTP(token: string, otp: string) {
  const decoded = jwt.verify(token, JWT_SECRET);
  const key = `share_otp:${decoded.shareId}`;
  
  const storedData = await redis.get(key);
  if (!storedData) {
    throw new Error('OTP expired');
  }
  
  const otpData = JSON.parse(storedData);
  
  if (otpData.attempts >= 3) {
    throw new Error('Maximum attempts exceeded');
  }
  
  otpData.attempts++;
  await redis.setex(key, 300, JSON.stringify(otpData));
  
  if (otpData.otp !== otp) {
    throw new Error('Invalid OTP');
  }
  
  // OTP verified - delete from Redis
  await redis.del(key);
  
  // Log access
  await db.medical_share_access_log.create({
    id: uuid(),
    share_id: decoded.shareId,
    patient_id: decoded.patientId,
    accessed_at: new Date(),
    ip_address: req.ip,
    user_agent: req.headers['user-agent']
  });
  
  // Fetch records
  const records = await fetchMedicalRecords(
    decoded.patientId,
    decoded.recordIds,
    decoded.recordTypes
  );
  
  return {
    patientInfo: {
      name: patient.name,
      age: calculateAge(patient.dateOfBirth),
      gender: patient.gender,
      bloodGroup: patient.bloodGroup
    },
    records: records,
    accessExpiresAt: new Date(Date.now() + 15 * 60 * 1000) // 15 min session
  };
}
```

**Frontend - QR Generation**:
```typescript
const QRShareModal = ({ patientId }) => {
  const [selectedRecords, setSelectedRecords] = useState([]);
  const [qrCode, setQRCode] = useState(null);
  
  const handleGenerate = async () => {
    const result = await api.generateMedicalShareQR({
      patientId: patientId,
      recordIds: selectedRecords.map(r => r.id),
      recordTypes: ['PRESCRIPTIONS', 'LAB_REPORTS']
    });
    
    setQRCode(result.qrCodeImage);
  };
  
  return (
    <Modal>
      <h2>Share Medical Records</h2>
      <p>Select records to share:</p>
      
      <RecordSelector
        records={allRecords}
        selected={selectedRecords}
        onChange={setSelectedRecords}
      />
      
      {qrCode ? (
        <div>
          <img src={qrCode} alt="Share QR Code" />
          <p>Show this QR code to the healthcare provider</p>
          <p>They will need an OTP that will be sent to your phone</p>
          <p>Valid for 1 hour</p>
          <Button onClick={() => revokeAccess(qrCode.shareId)}>
            Revoke Access
          </Button>
        </div>
      ) : (
        <Button onClick={handleGenerate}>Generate QR Code</Button>
      )}
    </Modal>
  );
};
```

---

## Technology Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI (MUI) or Ant Design
- **State Management**: Redux Toolkit + RTK Query
- **Routing**: React Router v6
- **Forms**: React Hook Form + Zod validation
- **Real-time**: Socket.IO client
- **3D Avatar**: D-ID SDK / Synthesia
- **Voice**: Web Speech API + AWS Transcribe
- **QR**: qrcode.react, react-qr-scanner
- **Signature**: react-signature-canvas
- **Build**: Vite
- **Testing**: Jest + React Testing Library
- **E2E**: Playwright

### Backend
- **Framework**: NestJS (Node.js + TypeScript)
- **API**: REST + GraphQL (Apollo Server)
- **Authentication**: AWS Cognito + JWT
- **Validation**: class-validator + class-transformer
- **ORM**: Prisma (PostgreSQL) + Mongoose (MongoDB)
- **Caching**: Redis (ioredis)
- **Queue**: Bull (Redis-based)
- **Logging**: Winston + Morgan
- **Monitoring**: Datadog / New Relic
- **Documentation**: Swagger (OpenAPI 3.0)
- **Testing**: Jest + Supertest

### Databases
- **Relational**: PostgreSQL 14+ (AWS RDS Multi-AZ)
- **Document**: MongoDB Atlas (M10 cluster)
- **Vector**: Pinecone (medical knowledge embeddings)
- **Cache**: Redis 7+ (AWS ElastiCache)
- **Analytics**: AWS Redshift / Snowflake
- **Search**: Elasticsearch 8.x (medicine catalog)

### Cloud Infrastructure (AWS)
- **Compute**: ECS Fargate (containers)
- **API Gateway**: AWS API Gateway
- **CDN**: CloudFront
- **Storage**: S3 (prescriptions, reports, signatures)
- **Functions**: Lambda (async tasks, ETL)
- **Queue**: SQS + SNS
- **Secrets**: AWS Secrets Manager
- **Monitoring**: CloudWatch + X-Ray
- **WAF**: AWS WAF + Shield

### AI/ML Services
- **LLM**: OpenAI GPT-4 / GPT-4-turbo
- **Embeddings**: OpenAI text-embedding-ada-002
- **Speech-to-Text**: AWS Transcribe
- **Text-to-Speech**: AWS Polly (Neural)
- **Avatar**: D-ID API
- **Medical NLP**: AWS Comprehend Medical (optional)

### External Integrations
- **Payments**: Razorpay (India), Stripe (Global)
- **SMS**: MSG91, Twilio
- **Email**: AWS SES, SendGrid
- **eSign**: e-Mudhra, NSDL e-Gov
- **KYC**: Surepass, AuthBridge, Signzy
- **Lab Partners**: Thyrocare, Dr. Lal PathLabs APIs
- **Logistics**: Dunzo, Porter, Shadowfax APIs
- **Maps**: Google Maps Platform
- **Analytics**: Mixpanel, Amplitude
- **Error Tracking**: Sentry
- **Push Notifications**: Firebase Cloud Messaging

---

## Security & Compliance

### Data Security

**Encryption**:
- At Rest: AES-256 (AWS KMS)
- In Transit: TLS 1.3
- Database: Encrypted storage (RDS encryption)
- Field-level: PHI fields double-encrypted

**Access Control**:
- Role-Based Access Control (RBAC)
- JWT tokens with short expiry (15 min)
- Refresh tokens (7 days, rotated)
- API rate limiting (100 req/min per user)
- IP whitelisting for admin access

**PHI Protection**:
- Masked in logs (automatic redaction)
- Minimum data exposure principle
- Audit trails for all PHI access
- Data retention policies (7 years for medical records)
- Right to deletion (GDPR-compliant)

### Compliance

**India**:
- Digital Personal Data Protection Act 2023
- Information Technology Act 2000
- Indian Medical Council regulations
- Telemedicine Practice Guidelines 2020
- PPI guidelines (wallet system)
- Drugs and Cosmetics Act compliance

**Global (Phase 2)**:
- HIPAA (USA)
- GDPR (Europe)
- PDPA (Singapore)
- Healthcare standards (HL7 FHIR)

### Audit & Logging

**Audit Events**:
```typescript
enum AuditEvent {
  // Patient events
  PATIENT_REGISTERED = 'patient_registered',
  CONSULTATION_STARTED = 'consultation_started',
  PRESCRIPTION_VIEWED = 'prescription_viewed',
  MEDICAL_RECORD_SHARED = 'medical_record_shared',
  
  // Physician events
  PRESCRIPTION_APPROVED = 'prescription_approved',
  PRESCRIPTION_REJECTED = 'prescription_rejected',
  PRESCRIPTION_MODIFIED = 'prescription_modified',
  
  // Data access
  PHI_ACCESSED = 'phi_accessed',
  PHI_EXPORTED = 'phi_exported',
  
  // System events
  PAYMENT_PROCESSED = 'payment_processed',
  ORDER_COMPLETED = 'order_completed',
  SIGNATURE_CAPTURED = 'signature_captured'
}

interface AuditLog {
  id: string;
  event: AuditEvent;
  actor_id: string;
  actor_role: UserRole;
  entity_type: string;
  entity_id: string;
  action: string;
  ip_address: string;
  user_agent: string;
  metadata: any;
  timestamp: Date;
}
```

**Immutable Audit Trail**:
- All audit logs append-only
- Write to S3 (versioned, locked)
- Cryptographic chaining (blockchain-inspired)
- Regular compliance audits

---

## Scalability & Performance

### Target Metrics
- **Consultation Capacity**: 10,000/day
- **API Response Time**: p99 < 500ms
- **AI Response Time**: p99 < 2s
- **Uptime**: 99.9% (8.7 hours/year downtime)
- **Concurrent Users**: 1,000

### Scaling Strategy

**Horizontal Scaling**:
```
ECS Fargate Auto-Scaling:
- Min: 3 tasks
- Max: 20 tasks
- Target CPU: 70%
- Scale up: +2 tasks if CPU > 70% for 2 min
- Scale down: -1 task if CPU < 30% for 5 min
```

**Database Optimization**:
```sql
-- Critical indexes
CREATE INDEX idx_consultations_patient_status 
  ON consultations(patient_id, status) WHERE status = 'ACTIVE';

CREATE INDEX idx_prescriptions_physician_pending
  ON prescriptions(physician_id, status) WHERE status = 'PENDING';

CREATE INDEX idx_orders_status_created
  ON orders(status, created_at DESC) WHERE status IN ('PLACED', 'CONFIRMED');

-- Partitioning (for large tables)
CREATE TABLE audit_logs_2025_01 PARTITION OF audit_logs
  FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
```

**Caching Strategy**:
```typescript
// Redis caching layers
const CACHE_TTL = {
  PATIENT_PROFILE: 60 * 15,        // 15 minutes
  MEDICINE_CATALOG: 60 * 60 * 24,  // 24 hours
  LAB_TESTS: 60 * 60 * 12,         // 12 hours
  PHYSICIAN_QUEUE: 60 * 2,         // 2 minutes
  STATIC_CONTENT: 60 * 60 * 24 * 7 // 7 days
};

async function getPatientProfile(patientId: string) {
  const cacheKey = `patient:${patientId}:v1`;
  
  // Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }
  
  // Fetch from DB
  const patient = await db.patients.findOne({ id: patientId });
  
  // Store in cache
  await redis.setex(
    cacheKey,
    CACHE_TTL.PATIENT_PROFILE,
    JSON.stringify(patient)
  );
  
  return patient;
}
```

**CDN Strategy**:
- Static assets (images, JS, CSS) → CloudFront
- Medicine images → CloudFront with origin S3
- Prescription PDFs → CloudFront with signed URLs
- Cache invalidation on updates

---

## Monitoring & Observability

### Key Metrics

**System Health**:
- API latency (p50, p95, p99)
- Error rates by endpoint
- Database query time
- OpenAI API latency
- Cache hit rate

**Business Metrics**:
- Daily active users (DAU)
- Consultations started vs completed
- AI prescription approval rate
- Payment success rate
- Order delivery success rate

**AI Performance**:
- Average consultation time
- AI confidence distribution
- Emergency detection rate
- Prescription modification rate by physicians

### Alerting

```
Critical (PagerDuty - 24/7):
- API error rate > 5% for 5 minutes
- Database connection failures
- OpenAI API unavailable
- Payment gateway down
- ECS tasks < minimum threshold

Warning (Slack):
- API latency p99 > 3s for 10 minutes
- AI prescription approval rate < 80%
- Medicine inventory low
- High OTP failure rate

Info (Email digest):
- Daily metrics summary
- Unusual traffic patterns
- Feature usage stats
```

---

## Deployment Architecture

### Multi-Environment Setup

```
Development (dev)
  ↓
Staging (staging) ← QA Testing
  ↓
Production (prod) ← Gradual Rollout
```

### Production Architecture

```
┌─────────────────────────────────────────────────────┐
│          AWS Region: ap-south-1 (Mumbai)             │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────────────────────────────────────────────┐│
│  │  Route 53 (DNS)                                ││
│  │  api.healthcare.com                            ││
│  │  app.healthcare.com                            ││
│  └─────────────┬──────────────────────────────────┘│
│                │                                     │
│  ┌─────────────▼──────────────────────────────────┐│
│  │  CloudFront CDN                                ││
│  │  - SSL Termination (ACM)                       ││
│  │  - WAF Rules                                   ││
│  │  - DDoS Protection (Shield)                    ││
│  └─────────────┬──────────────────────────────────┘│
│                │                                     │
│  ┌─────────────▼──────────────────────────────────┐│
│  │  API Gateway                                   ││
│  │  - Rate Limiting                               ││
│  │  - Request/Response Validation                 ││
│  │  - CORS                                        ││
│  └─────────────┬──────────────────────────────────┘│
│                │                                     │
│  ┌─────────────▼──────────────────────────────────┐│
│  │  Application Load Balancer                     ││
│  │  - Health Checks                               ││
│  │  - SSL/TLS                                     ││
│  │  - Target Groups                               ││
│  └─────────────┬──────────────────────────────────┘│
│                │                                     │
│  ┌─────────────▼──────────────────────────────────┐│
│  │  VPC (10.0.0.0/16)                             ││
│  │  ┌──────────────────────────────────────────┐ ││
│  │  │  Public Subnets (3 AZs)                  │ ││
│  │  │  - NAT Gateways                          │ ││
│  │  │  - Bastion Hosts                         │ ││
│  │  └──────────────────────────────────────────┘ ││
│  │  ┌──────────────────────────────────────────┐ ││
│  │  │  Private Subnets (3 AZs)                 │ ││
│  │  │  ┌────────────────────────────────────┐ │ ││
│  │  │  │  ECS Fargate Cluster               │ │ ││
│  │  │  │  ┌──────────────┐ ┌──────────────┐ │ │ ││
│  │  │  │  │ API Service  │ │ API Service  │ │ │ ││
│  │  │  │  │  (Task 1)    │ │  (Task 2)    │ │ │ ││
│  │  │  │  └──────────────┘ └──────────────┘ │ │ ││
│  │  │  │  ┌──────────────┐                  │ │ ││
│  │  │  │  │ Worker Tasks │                  │ │ ││
│  │  │  │  └──────────────┘                  │ │ ││
│  │  │  └────────────────────────────────────┘ │ ││
│  │  │  ┌────────────────────────────────────┐ │ ││
│  │  │  │  RDS PostgreSQL (Multi-AZ)         │ │ ││
│  │  │  │  - Primary + Standby               │ │ ││
│  │  │  │  - Read Replica (optional)         │ │ ││
│  │  │  └────────────────────────────────────┘ │ ││
│  │  │  ┌────────────────────────────────────┐ │ ││
│  │  │  │  ElastiCache Redis (Cluster)       │ │ ││
│  │  │  │  - 3 nodes for HA                  │ │ ││
│  │  │  └────────────────────────────────────┘ │ ││
│  │  └──────────────────────────────────────────┘ ││
│  └────────────────────────────────────────────────┘│
│                                                      │
│  External Services:                                  │
│  - S3 (Prescriptions, Reports, Images)              │
│  - SQS/SNS (Message Queue)                          │
│  - Lambda (Async Processing)                        │
│  - CloudWatch (Logging, Monitoring)                 │
│  - Secrets Manager (Credentials)                    │
│  - KMS (Encryption Keys)                            │
└─────────────────────────────────────────────────────┘
```

---

## Cost Estimation (Monthly at Scale)

| Component | Specification | Monthly Cost (USD) |
|-----------|--------------|-------------------|
| **Compute** | | |
| ECS Fargate | 5 tasks × 2vCPU × 4GB | $300 |
| Lambda | 10M invocations | $100 |
| **Database** | | |
| RDS PostgreSQL | db.t3.large Multi-AZ | $250 |
| MongoDB Atlas | M10 cluster | $100 |
| Redis | cache.t3.medium (3 nodes) | $150 |
| Pinecone | 1M vectors | $70 |
| **Storage & CDN** | | |
| S3 | 1TB storage + 5TB transfer | $100 |
| CloudFront | 3TB data transfer | $200 |
| **API & Networking** | | |
| API Gateway | 100M requests | $100 |
| Data Transfer | VPC, NAT | $150 |
| **Monitoring** | | |
| CloudWatch | Logs + Metrics | $80 |
| Datadog | APM + Logs | $200 |
| **AWS Subtotal** | | **$1,800** |
| | | |
| **External Services** | | |
| OpenAI | 300K consults × $0.08 | $24,000 |
| D-ID Avatar | 300K sessions × $0.05 | $15,000 |
| AWS Transcribe | 300K × 5 min × $0.024/min | $36,000 |
| AWS Polly | 300K × 3 min × $0.016/min | $14,400 |
| Razorpay | 2% on ₹50M GMV | $12,000 |
| MSG91 SMS | 900K messages × $0.01 | $9,000 |
| Aadhaar eSign | 300K signatures × $0.10 | $30,000 |
| **External Subtotal** | | **$140,400** |
| | | |
| **TOTAL MONTHLY COST** | | **$142,200** |
| **Per Consultation Cost** | 10K/day = 300K/month | **$0.47** |

**Revenue Model** (at scale):
- Consultation: ₹99 ($1.20) × 300K = $360K
- Medicine commission: 15% on ₹400 AOV × 210K orders = $126K
- Lab commission: 15% on ₹800 AOV × 90K bookings = $108K
- **Total Revenue**: $594K/month
- **Gross Profit**: $451.8K (76% margin)

---

## Implementation Priority

### MVP (Day 1-45) - Must Have
1. ✅ AI Avatar Consultation
2. ✅ RAG Privacy Layer
3. ✅ Prescription Generation
4. ✅ Physician Review + eSign
5. ✅ Patient Signature
6. ✅ Medicine Catalog + Ordering
7. ✅ Payment Integration
8. ✅ Basic Wallet
9. ✅ OTP-on-Delivery

### Phase 2 (Day 46-90) - High Priority
10. Lab Testing Module
11. Family Accounts
12. QR Medical Sharing
13. Identity Verification (Aadhaar)
14. Merchant Settlement System
15. Gift Cards

### Phase 3 (Day 91-120) - Medium Priority
16. Genetic Testing
17. De-identified Analytics
18. Advertisement System
19. Push Notifications
20. White-Label Clinic Mode

### Phase 4 (Month 6+) - Nice to Have
21. Mobile App (React Native)
22. Video Consultations
23. Chronic Disease Management
24. Insurance Integration
25. International Expansion

---

## Success Metrics

**Technical KPIs**:
- System uptime: > 99.9%
- API latency p99: < 500ms
- AI consultation completion rate: > 85%
- Payment success rate: > 95%
- Error rate: < 1%

**Business KPIs**:
- Daily consultations: 10,000
- Prescription approval rate: > 90%
- Medicine order conversion: > 60%
- Customer satisfaction (NPS): > 50
- Average order value: ₹400+

**Medical Safety KPIs**:
- Zero controlled substance prescriptions by AI
- Zero adverse event escalations
- 100% physician review for critical conditions
- Emergency detection accuracy: 100%
- Allergy conflict prevention: 100%

---

## Conclusion

This high-level design provides a comprehensive blueprint for building a full-featured AI-powered healthcare platform. The architecture is designed for:

1. **Scalability**: Handle 10K+ daily consultations
2. **Security**: PHI protection, encryption, compliance
3. **Reliability**: Multi-AZ, auto-recovery, 99.9% uptime
4. **Extensibility**: Easy to add new features while live
5. **Cost-Efficiency**: $0.47 per consultation cost, 76% gross margin

The system balances AI efficiency with medical oversight, ensuring both rapid consultation delivery and patient safety. The modular architecture allows for rapid MVP delivery (45 days) while supporting continuous feature rollout post-launch.

**Next Steps**: Proceed to Low-Level Design for detailed implementation specifications.