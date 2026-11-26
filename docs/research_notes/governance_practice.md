# How hospitals run data protection and AI governance in practice (Qatar and Gulf first, then leading international examples)

Research date: 22 November 2026. Each finding says whether it is **[QATAR]**, **[GULF]** (other GCC) or **[INTL]** (international), and gives the date of the source. Material from before 2024 is marked **(older)**. Several primary pages could not be fetched (PDF parsing failures, HTTP 403, firewall blocks). Where a finding relies only on a search-engine summary, it is marked **(search summary)** and should be checked before anyone quotes it word for word.

---

## 1. Governance roles and bodies: DPO or privacy officer, data governance committees, clinical AI oversight committees, NHS Caldicott model, Qatari providers

### Takeaway
Qatar's law (PDPPL, Law No. 13 of 2016) does not require a Data Protection Officer. Qatar's largest provider, HMC, publishes a privacy notice and numbered internal policies but names no DPO and no AI governance committee. National AI governance in Qatar happens at strategy and committee level (MCIT AI Committee, NCSA, MoPH), not hospital by hospital. The most detailed working models are international: the NHS Caldicott Guardian, SIRO and DPO triad; Duke Health's ABCDS algorithm-oversight committee; and the 2025 Joint Commission + CHAI guidance, which calls for a multidisciplinary AI governance body that reports to the board.

### Cited Findings

**Qatar: legal roles and the regulator**
- [QATAR] The PDPPL contains no express obligation for organisations in Qatar to appoint a data protection officer. The separate QFC regime does have a DPO concept. — [DLA Piper Data Protection Laws of the World: Qatar](https://www.dlapiperdataprotection.com/?c=QA&t=law); [Chambers Data Protection & Privacy 2026: Qatar](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice) (search summary)
- [QATAR] HMC's privacy notice directs privacy queries to "National Cyber Governance and Assurance Affairs" (PO Box 24100, Doha; privacy@ncsa.gov.qa). This is a primary document showing that the National Cyber Security Agency (NCSA) is now the privacy authority patients are pointed to. — [HMC Privacy Notice, last updated 9 Jan 2025](https://hamad.qa/EN/Patient-Information/Patient-Family-Rights/Pages/HMC-Privacy-Notice.aspx)
- [QATAR] **(older, 2020–21)** In November 2020 the Compliance and Data Protection Department (CDP) of the then Ministry of Transport and Communications issued 14 PDPPL guidelines. They require controllers to: carry out a DPIA before new processing, particularly for special-nature data or prospective data exports; keep a record of processing activities (ROPA) and train departments to update it; notify breaches to the CDP and affected individuals within 72 hours; carry out due diligence on processors and put adequate contracts in place; build privacy in "from the design stage"; and answer data-subject requests within 30 days. Processing special-nature data (including health data) needs CDP authorisation via a Special Nature Personal Data Form. — [Clyde & Co, 15 Mar 2021](https://www.clydeco.com/en/insights/2021/03/new-regulatory-guidelines-on-the-qatar-persona-1)
- [QATAR] NCSA publishes a DPIA template and a ROPA template. — [PwC Data Privacy Handbook: Qatar](https://www.pwc.com/m1/en/services/consulting/technology/cyber-security/documents/pwc-data-privacy-book-qatar-english.pdf) (search summary)

**Qatar: Hamad Medical Corporation (HMC)**
- [QATAR] HMC Privacy Notice (last updated 9 January 2025):
  - It cites PDPPL No. 13/2016.
  - Lawful purposes listed include explicit consent (e.g., through the Release of Information process: "HMC will share your personal information if you give specific consent for us to do so"), vital interests, preventive/occupational medicine, public-safety emergencies, population health management, public health surveillance, scientific research, education, legal investigations and legal obligations.
  - Recipients include other providers "and parties involved in your care, including insurers", vendors and contractors, and government, regulators, courts and law enforcement "when required by law".
  - "Aggregated or anonymized data" may be shared for research and statistics.
  - Data is stored on servers "located in Qatar or in other countries that have adequate data protection laws".
  - Retention is "Indefinitely for Qatari Nationals, 10 years for non-Qatari nationals".
  - **No DPO is named.** The contact is Nesmaak@hamad.qa / 16060.
  - The notice does **not mention AI or automated decision-making.**
  - — [HMC Privacy Notice](https://hamad.qa/EN/Patient-Information/Patient-Family-Rights/Pages/HMC-Privacy-Notice.aspx)
- [QATAR] HMC's internal policy references include **OP 4042 "Privacy, Confidentiality and Access to Health Information"** and **CL 7226 "Informed Consent"**. Medical information "may be released to the patient or any other person authorized in writing". A minor's or incompetent person's authorisation comes from the legal guardian. — [HMC Medical Reports Guidelines](https://www.hamad.qa/EN/Medical-Reports/Pages/Guidelines.aspx)
- [QATAR] HMC policy **OP 4044** (CPD participant privacy, dated 23 Aug 2020 **(older)**) says participant information should not be shared with commercial entities or sponsors. — [HMC OP 4044](https://hamad.qa/EN/Education-and-research/Medical-Education/CPD/CPD-Organizers/HMC-CPD-Toolkit-A/Pages/A6.aspx) (search summary)
- [QATAR] HMC patient-rights pages give patients the right to request amendment of their records under HMC policy. They also let patients choose a family member or legal representative to be present when medical information is discussed. — [HMC Patient and Family Rights](https://hamad.qa/EN/Hospitals-and-services/Heart%20Hospital/Patients%20and%20Visitors/General_information/Pages/Patient-and-Family-Rights.aspx) (search summary)
- [QATAR] HMC and PHCC share a centralised EHR system. HBKU's Qatar Computing Research Institute (QCRI) says this makes it possible to build AI prediction models from EHR data. — [HBKU/QCRI project page](https://elmi.hbku.edu.qa/en/projects/artificial-intelligence-for-precision-medicine-health-technologie/) (search summary)

**Qatar: national AI governance (what exists above the hospital level)**
- [QATAR] A Jan 2026 narrative review by an HMC author (Mohamed A. Ismail, *Frontiers in AI* 9, DOI 10.3389/frai.2026.1702242) describes:
  - the 2019 National AI Strategy, with six pillars, one of which is ethics and public policy;
  - an **Artificial Intelligence Committee established in 2021** "to oversee the integration of AI across all sectors";
  - the **National Health Strategy 2024–2030**;
  - NCSA's **"Guidelines for Secure Usage and Adoption of AI"**, built on transparency, accountability, fairness and robustness.

  It also states that the health ministry, together with the Communications Regulatory Authority (CRA), applies "a risk-tiered system to regulate the use of AI in the healthcare field". That claim rests on a single secondary citation and comes with no detail. The review gives inconsistent dates for the PDPPL (2016 vs 2017). — [Frontiers in AI, 27 Jan 2026](https://www.frontiersin.org/articles/10.3389/frai.2026.1702242/full)
- [QATAR] The same review lists provider AI activity but no provider-level governance bodies:
  - HMC: AI-equipped adaptive radiotherapy at the National Center for Cancer Care and Research, a Center of Clinical Precision Medicine and Genomics, and the Lbaih app.
  - Sidra Medicine: an AI dynamic risk score for Type 1 diabetes and the POST hypospadias planning tool.
  - PHCC: Droobi/Lillia digital therapeutics and the Nar'aakom portal.

  Aspetar is not mentioned. — [Frontiers in AI, Jan 2026](https://www.frontiersin.org/articles/10.3389/frai.2026.1702242/full)
- [QATAR] HBKU's College of Law, in partnership with MoPH, produced the **"Research Guidelines for Healthcare AI Development"**. These encourage developers to "follow detailed processes and document the purpose, scope, and intended use of AI systems" and to consider ethics and data-protection law from the outset. HBKU researchers (Dr Barry Solaiman) separately proposed a "True Lifecycle Approach": governance across R&D, systems approval, and use in practice, with rules reaching providers and insurers. That approach is a **proposal, not adopted policy**. — [Gulf Times, 8 Aug 2025](https://www.gulf-times.com/article/708627/qatar/new-model-of-governance-for-ai-in-healthcare-proposed); [Diplomatic Courier](https://diplomaticourier.com/posts/a-true-lifecycle-approach-for-governing-healthcare-ai)
- [QATAR] **(Dec 2024)** MoPH held a National Health Research Ethics Workshop on AI in health research, data management and national policies, with NCSA and Qatar University. — [QNA, 1 Dec 2024](https://www.qna.org.qa/en/News-Area/News/2024-12/01/0057-moph-discusses-ethics-of-use-of-artificial-intelligence-in-health-research)
- [QATAR] Sidra Medicine (Nov 2026) contributed 100 anonymised neonatal chest X-rays to a Harvard-led international AI study. The method lets hospitals contribute to model development "without centralising patient imaging data". No published Sidra AI-governance policy was found. Sidra's online privacy policy covers only website and app data. — [QNA, 11 Nov 2026](https://qna.org.qa/en/News-Area/News/2026-11/11/sidra-medicine-contributes-to-international-ai-study-advancing-neonatal-care); [Sidra Privacy Policy](https://www.sidra.org/?p=3)
- [QATAR] **(older, 2023)** PHCC describes a "Centralized Health Intelligence" framework, with an enterprise data warehouse and BI tools in its Business Health Intelligence (BHI) Department that "improved data governance". No PHCC AI strategy was found. — [Qatar Journal of Public Health 2023](https://qscience.com/content/journals/10.5339/qjph.2023.8)

**Gulf comparators**
- [GULF] Abu Dhabi Department of Health issued a **Responsible AI Standard, effective October 2025**. — [DoH Abu Dhabi document](https://www.doh.gov.ae/-/media/B84FF5DD027846699C51F36C439A580F.ashx) (search summary; contents not reviewed)
- [GULF] **(2022)** The Dubai Health Authority publishes an *Artificial Intelligence Policy*, a *Health Data Protection and Confidentiality Policy* and a *Health Data Classification Policy*. — [DHA AI Policy](https://www.dha.gov.ae/uploads/082022/Artificial%20Intelligence%20Policy20228457.pdf); [DHA Health Data Protection and Confidentiality Policy](https://www.dha.gov.ae/uploads/082022/Health%20Data%20Protection%20and%20Confidentiality%20Policy_EN2022810559.pdf); [DHA Health Data Classification Policy](https://www.dha.gov.ae/uploads/082022/Health%20Data%20Classification%20Policy2022852434.pdf) (existence confirmed from search results only; contents not reviewed)

**International: NHS information-governance model**
- [INTL] **Eight Caldicott Principles** (National Data Guardian, 8 Dec 2020, England):
  1. Justify the purpose(s) for using confidential information.
  2. Use confidential information only when it is necessary.
  3. Use the minimum necessary confidential information.
  4. Access on a strict need-to-know basis ("access controls or split information flows" may help).
  5. Everyone with access should be aware of their responsibilities.
  6. Comply with the law.
  7. The duty to share information for individual care is as important as the duty to protect patient confidentiality.
  8. **"Inform patients and service users about how their confidential information is used"**: "a range of steps should be taken to ensure no surprises for patients and service users, so they can have clear expectations about how and why their confidential information is used, and what choices they have about this."

  Principle 1 says continuing uses should be reviewed "by an appropriate guardian". — [GOV.UK: The Caldicott Principles](https://www.gov.uk/government/publications/the-caldicott-principles); [Eight Caldicott Principles PDF](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/942217/Eight_Caldicott_Principles_08.12.20.pdf)
- [INTL] The NDG consultation response says Principle 8 was added to emphasise the patient's perspective. Patients "should be included as active partners in the use of confidential information". — [NDG press release](https://gov.uk/government/news/ndg-announces-new-caldicott-principle-and-guidance-on-caldicott-guardians); [Consultation response PDF](https://assets.publishing.service.gov.uk/media/5fcf52a4e90e07562074768a/NDG_CP_and_CG_consultation_response_FINAL_08.12.20.pdf)
- [INTL] **NDG guidance on Caldicott Guardians (v1.0, 27 Aug 2021).** It was issued under statutory powers, so in-scope bodies "must have regard" to it.
  - Who should appoint one (s3.1): all public bodies in England's health service, adult social care or carer support that process confidential patient data, plus organisations contracted to deliver publicly funded services.
  - Day-to-day activities (s4.4): "advising on disclosures of confidential information"; patient complaints; "reviewing and advising on data protection impact assessments, data sharing agreements, and instructions to data processors"; audit; and "involvement in data breach investigations".
  - Relationship to the **SIRO** (an executive or board member who owns information risk): "It would not normally be appropriate for the same person to be both SIRO and Caldicott Guardian, due to the possibility of a conflict of interest" (s5.3).
  - Relationship to the **DPO** (advises on and monitors compliance with data-protection law): a Guardian "may also be appointed as Data Protection Officer, but care must be taken to ensure that no conflict of interest arises" (s5.5).
  - Independence and support: Guardians "must be free to raise concerns at senior management or board level" and "should not be dismissed or penalised… for performing their role" (s6, s8.3).
  - Organisations should consider appointing a deputy (s3.6), should enable "meaningful and effective engagement with patients" (s8.4), and Guardians should document advice given (s6.5).
  - — [NDG Caldicott Guardian guidance PDF, 27 Aug 2021](https://assets.publishing.service.gov.uk/media/6127b6d6e90e0705437230da/Caldicott_Guardian_guidance_v1.0_27.08.21.pdf); [GOV.UK page](https://www.gov.uk/government/publications/national-data-guardian-guidance-on-the-appointment-of-caldicott-guardians-their-role-and-responsibilities)
- [INTL] In-scope organisations were expected to have a Caldicott Guardian in place by 30 June 2023. — [Digital Health News](https://digitalhealth.net/?p=124615) (search summary)

**International: clinical AI and algorithm oversight committees**
- [INTL] **Joint Commission + Coalition for Health AI (CHAI), "Responsible Use of AI in Healthcare" guidance (2025; non-binding).** It sets out seven elements:
  1. AI governance structures
  2. patient privacy and transparency
  3. data security
  4. ongoing quality monitoring
  5. voluntary, blinded reporting of AI safety events
  6. risk and bias assessment
  7. education and training

  It recommends a "multi-disciplinary governance body to lead and monitor the selection, implementation and use of AI tools" that reports to senior leadership and the board. Organisations should validate each tool before deployment by reviewing the vendor's testing, validation and bias assessments, and treat AI as "dynamic systems requiring continuous oversight". A voluntary AI certification and governance "playbooks" are planned.

  Fenwick (5 Nov 2025) adds more detail:
  - The governance structure should keep "the hospital's governing body aware of uses, outcomes, and potential drawbacks of health AI tools" and include executive leadership, compliance, IT, cybersecurity, safety, and clinical and operational staff.
  - Patients should be **notified** when AI directly affects their care and told how their data may be used. The guidance describes notification, not consent.
  - Limit permitted uses of exported data: "Even when data is properly de-identified under HIPAA, organizations should apply strong protections", with "contractual guardrails", especially on re-identification.
  - During procurement, obtain the vendor's testing, validation and bias-mitigation evidence, and ask whether the vendor will tune or validate on a representative local sample. After deployment, run risk-based monitoring.
  - Check for bias using local data, and "consider whether the training datasets were fit for purpose and representative".
  - Report AI safety events voluntarily, e.g., via the Joint Commission sentinel-event process or confidentially to Patient Safety Organizations.

  — [Fenwick, 5 Nov 2025](https://www.fenwick.com/insights/publications/joint-commission-and-chai-release-guidance-on-responsible-use-of-ai-in-healthcare); [Becker's Hospital Review](https://www.beckershospitalreview.com/healthcare-information-technology/ai/joint-commission-issues-ai-guidance-for-healthcare-organizations/); [Polsinelli](https://www.polsinelli.com/publications/tjc-chai-release-guidance-responsible-ai-use-healthcare); [Fenwick](https://www.fenwick.com/insights/publications/joint-commission-and-chai-release-guidance-on-responsible-use-of-ai-in-healthcare) (law-firm and trade summaries; primary document not fetched)
- [INTL] **Duke Health ABCDS** (Algorithm-Based Clinical Decision Support) Oversight:
  - It keeps "a registry of all algorithmic solutions under consideration for use in patient care at Duke Health".
  - An **Implementation Subcommittee** triages each registration into "Full review (high risk)", "Fast-track review (moderate risk)" or "Registration only (low risk)". For low-risk tools, the Clinical and Model Owners must do independent validation themselves.
  - An **independent Review Committee** evaluates at lifecycle checkpoints: *Impact Potential → Real-World Readiness → Real-World Impact → Sustained Impact*.
  - Possible decisions are Approval, Approval with contingencies, Re-Review, or Decline, with "details of and a timeline to resolve gaps".
  - A Bias Management Framework is used as guidance.
  - — [Duke ABCDS Oversight Process](https://healthaigovernance.duke.edu/abcds-oversight/abcds-oversight-process)
- [INTL] The ABCDS Oversight Committee is co-chaired by Michael Pencina and Eric Poon, with clinical, operational, data-science and legal members and three specialised subcommittees. It reviews both in-house and vendor tools. — [Duke AI Health: ABCDS Oversight Committee](https://aihealth.duke.edu/the-abcds-oversight-committee); [What is ABCDS?](https://aihealth.duke.edu/algorithm-based-clinical-decision-support-abcds) (search summary)
- [INTL] **NHS England, guidance on AI-enabled ambient scribing** (first version 27 Apr 2025; updated 24 Mar 2026, developed with ICO and NDG input). Deploying organisations should:
  - appoint a **Clinical Safety Officer**;
  - complete **DCB0160** documentation (safety case, hazard log, monitoring framework) and a **DPIA**;
  - confirm the supplier has completed **DCB0129**.

  The guidance also says:
  - Generative-AI summarisation "likely would qualify as a medical device" (MHRA registration).
  - The 2026 update says explicit consent is not required for individual care, but transparency is essential, and if a patient dissents the tool cannot be used for them.
  - A national Ambient Voice Technology (AVT) supplier registry exists.

  — [NHS England publication page](https://www.england.nhs.uk/publication/guidance-on-the-use-of-ai-enabled-ambient-scribing-products/); [Digital Health News, Apr 2026](https://www.digitalhealth.net/2026/04/nhse-publishes-fresh-guidance-on-safe-use-of-ambient-scribes/); [HTN, 28 Apr 2025](https://htn.co.uk/2025/04/28/ambient-voice-technology-guidance-launched-by-nhse-to-support-adoption/) (search summaries; primary page did not render)

### Inferences
- No Qatari hospital publishes an AI-governance committee charter or a named DPO. A Qatari gateway policy therefore has to **define these roles itself**, citing the PDPPL guidelines (DPIA, ROPA, processor contracts, 72-hour breach notice, special-nature authorisation) as the legal anchor. NHS and Duke structures can serve as the design model.
- A workable role set for the gateway, adapted from the NHS triad:
  - a **DPO / Privacy Officer**, who owns PDPPL compliance, DPIAs, the ROPA and NCSA liaison;
  - a **Clinical Confidentiality Guardian** modelled on the Caldicott Guardian: a senior clinician who advises on difficult disclosures, reviews data-sharing agreements and channel loosening requests, and is protected from penalty;
  - a **Senior Information Risk Owner**, an executive who owns information risk and is kept separate from the Guardian to avoid conflict;
  - a **Clinical AI Oversight Committee**, multidisciplinary, reporting to the board, running Duke-style risk triage and checkpoints for each gateway channel (AI diagnostic tool, insurer, MoPH).
- Caldicott Principle 8 ("no surprises") maps directly onto a patient-facing gateway notice. HMC's current notice does not mention AI or automated processing, which is a gap the policy could close.
- HMC's retention rule (indefinite for nationals, 10 years for others) shows that **nationality is already a policy-relevant attribute** in Qatari health records. That reinforces treating nationality as a quasi-identifier in small populations.

### Gaps
- No published AI-governance policy, AI committee charter or AI centre-of-excellence terms of reference was found for HMC, Sidra, PHCC or Aspetar. Aspetar returned nothing relevant.
- The full text of HMC OP 4042 and of the MoPH/HBKU "Research Guidelines for Healthcare AI Development" was not found online.
- No current (2025–26) NCSA document was found that confirms whether a DPO is now expected. The "risk-tiered" MoPH/CRA AI regulation claim could not be verified from a primary source.
- The primary text of the Joint Commission/CHAI guidance and the NHS ambient-scribe page did not render, so only summaries were used.

---

## 2. Processes: DPIAs for AI tools, data-sharing agreements, release of information, access logging and audit, breach response, periodic re-identification review, post-deployment monitoring, human-in-the-loop escalation

### Takeaway
Every mature framework found requires a DPIA **before** an AI tool goes live, and the Qatar guidelines require one for any new processing of special-nature data. A senior privacy or clinical role (DPO and/or Guardian) reviews the DPIA and the data-sharing agreements. Breach notice in Qatar is 72 hours under the 2021 guidelines. Re-identification risk and AI performance are treated as **changing over time** and must be re-reviewed on a schedule, not certified once.

### Cited Findings
- [QATAR] **(2020–21 guidelines)** A DPIA is required "before undertaking new processing activities", especially for special-nature data or exports. Clyde & Co cite a possible QAR 1,000,000 fine for failing to do one. The guidelines also require a ROPA, privacy by design, processor due diligence and contracts, and breach notification to the CDP and affected individuals within 72 hours. — [Clyde & Co, Mar 2021](https://www.clydeco.com/en/insights/2021/03/new-regulatory-guidelines-on-the-qatar-persona-1)
- [QATAR] **Release of information at HMC.** The patient or an authorised representative completes an online "Consent for Release of Medical Information" form and attaches copies of the patient's QID or passport. A representative also attaches their own QID or passport and an authorisation letter. Originals must be shown to Health Information Management staff at collection. Payment is by credit card. Requesters "shall be responsible for all liabilities and claims" arising from obtaining the information. Timelines and third-party (insurer, employer, court) procedures are not published on that page. — [HMC Medical Reports Guidelines](https://www.hamad.qa/EN/Medical-Reports/Pages/Guidelines.aspx)
- [QATAR] Within HMC's Communicable Disease Center, the patient decides which family member or friend may access their record, and nurses obtain written consent first. — [HMC "Access to Privacy" leaflet](https://www.hamad.qa/EN/Hospitals-and-services/Communicable-Disease-Center/Documents/ACCESS-TO-PRIVACY.pdf) (search summary)
- [INTL] Caldicott Guardians review and advise on "data protection impact assessments, data sharing agreements, and instructions to data processors", and take part in "audit reporting" and "data breach investigations", alongside the DPO. — [NDG Caldicott Guardian guidance, 2021](https://assets.publishing.service.gov.uk/media/6127b6d6e90e0705437230da/Caldicott_Guardian_guidance_v1.0_27.08.21.pdf)
- [INTL] For ambient AI scribes, NHS England expects a DPIA and DCB0160 clinical-safety documentation, including a **hazard log and monitoring framework**, before deployment. An earlier June 2025 NHS notification said liability for non-compliant solutions sits with the deploying organisation or clinician. — [NHS England publication page](https://www.england.nhs.uk/publication/guidance-on-the-use-of-ai-enabled-ambient-scribing-products/); [SSL LMCs summary](https://www.sslmcs.co.uk/?p=4977) (search summaries)
- [INTL] **Periodic re-identification review.** The ICO's anonymisation guidance (2025) uses the "motivated intruder" test: a reasonably competent intruder with ordinary resources such as the internet and public documents. It names singling out and linkability as the key indicators of identifiability. It says identifiability "can change over time due to technological advancements and the availability of additional data" and that organisations should "review your risk assessments and decision-making processes regularly". Pinsent Masons notes the guidance treats **generative AI tools** as among the "obvious sources" an intruder has. The ICO marks the guidance as under review following the Data (Use and Access) Act (19 June 2025), and it is not a statutory code. — [ICO: How do we ensure anonymisation is effective?](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/how-do-we-ensure-anonymisation-is-effective); [ICO: About this guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/about-this-guidance/); [Pinsent Masons Out-Law](https://www.pinsentmasons.com/out-law/analysis/ico-anonymisation-guide-uk-data-protection-compliance)
- [INTL] **Post-deployment monitoring.** Joint Commission/CHAI: evaluate AI tools for risk and bias "before and after implementation". Duke ABCDS has a "Sustained Impact" checkpoint and keeps tools in a registry through monitoring and maintenance. — [Polsinelli summary](https://www.polsinelli.com/publications/tjc-chai-release-guidance-responsible-ai-use-healthcare); [Duke ABCDS process](https://healthaigovernance.duke.edu/abcds-oversight/abcds-oversight-process)
- [INTL] A 2024 bowtie analysis of automation bias in AI clinical decision support sets out preventive controls during model design and mitigation controls after deployment. It notes that quantitative evaluation of those controls is still future work. — [Abdelwanis et al. 2024, bowtie analysis](https://libraries.escp.eu/doc/edselp/S2666449624000410) (search summary)
- [INTL] **Incident reporting for AI.** The Joint Commission/CHAI guidance encourages voluntary, confidential reporting of AI safety events, for example to patient-safety organisations. — [Becker's](https://www.beckershospitalreview.com/healthcare-information-technology/ai/joint-commission-issues-ai-guidance-for-healthcare-organizations/)
- [INTL] **Human-in-the-loop requirements in law (EU AI Act Art. 14).** Overseers of high-risk AI must:
  - "remain aware of the possible tendency of automatically relying or over-relying on the output" (automation bias, 14(4)(b));
  - be able to "disregard, override or reverse the output" (14(4)(d));
  - be able to "interrupt the system through a 'stop' button or a similar procedure" (14(4)(e)).

  For remote biometric identification only, two competent people must separately verify a match (14(5)). The site gives application dates of 2 Dec 2027 for Annex III systems and 2 Aug 2028 for Annex I (product-embedded, e.g., medical-device) systems. — [AI Act Article 14](https://artificialintelligenceact.eu/article/14/)
- [INTL] **Access logging (US model).** The HIPAA Security Rule "audit controls" standard requires mechanisms that "record and examine activity in information systems that contain or use electronic protected health information". — [45 CFR 164.312(b), eCFR](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-C/section-164.312) (regulation text; not re-fetched in this session)

### Inferences
A gateway policy can lay out a process cycle from these sources:
1. **Register** every channel and model with the oversight committee (Duke registry).
2. **Triage risk**: the deep AI-tool channel gets full review, the insurer and MoPH channels fast-track (Duke).
3. Complete a **DPIA plus clinical-safety case and hazard log** before go-live (Qatar guidelines, NHS DCB0160).
4. Have the Guardian or DPO **review the data-sharing agreement** for each external recipient (NDG).
5. **Log every release** with purpose, recipient, ruleset version and reviewer, retained for audit (HIPAA audit-controls model, Caldicott Principle 1 recorded purposes).
6. Treat **breach or near-miss** (e.g., a leaked identifier found in an outbound payload) as a 72-hour notifiable event if personal data left the hospital (Qatar guidelines).
7. **Re-test re-identification risk on a schedule and on trigger**: new outside model, new public data source, ruleset change. The ICO says identifiability changes over time and explicitly mentions generative AI as an intruder resource.
8. Give the **human reviewer stop and override authority** and an escalation path (AI Act Art. 14).

The 72-hour Qatar breach window is shorter than the HIPAA 60-day individual-notice outer limit (not verified in this session). It suits a gateway that can detect leaks automatically.

### Gaps
- No Qatar-specific guidance was found on access-log retention periods, audit frequency, or periodic re-identification review.
- No published HMC timeline for release of information or for third-party (insurer, embassy, court) requests was found.
- It is unclear whether NCSA (which replaced the CDP) has re-issued or amended the 2020 guidelines (72-hour rule, DPIA rule). Other researchers covering PDPPL text should confirm.

---

## 3. Vendor and AI-tool contracts: DPA clauses for AI vendors, and good practice for sending de-identified data to LLM or AI APIs

### Takeaway
Law-firm guidance from 2025–26 agrees on a core clause set:
- an explicit **no-training default** covering prompts, inputs and outputs;
- precise definitions instead of vague "service improvement" rights;
- **deletion or return** at termination, with no surviving rights over models trained on the data unless expressly bargained for;
- flow-down of no-training terms to AI **sub-processors**;
- alignment with the health-privacy agreement, e.g., a US BAA.

Vendor commitments such as OpenAI's are a starting point, but they still allow up to **30-day abuse-monitoring retention** unless zero data retention (ZDR) is approved. Research data custodians (PhysioNet) treat even de-identified clinical text as **not to be sent to third-party LLM APIs** unless ZDR, no training and no human review are all verified, and they prefer local models.

### Cited Findings
- [INTL] **Foley & Lardner (25 June 2025):**
  - Define training use precisely; avoid "improving services" or "analytics purposes" language.
  - State whether data is identifiable or de-identified and which de-identification method applies.
  - Say whether learning from one client's data stays in that client's model or is pooled across the platform.
  - Align commercial terms with the BAA ("A mismatch… can raise compliance issues").
  - Make any post-termination right to use data or trained models "an express, bargained-for right".
  - Include a data return or destruction clause with timing and method.
  - Reject the argument that a trained model is no longer tied to its data.
  - Use a "tiered cap based on use case" rather than a 12-month-fees liability cap.
  - Add indemnities for privacy violations and regulatory enforcement.
  - Post-termination licences in health care "will generally involve only de-identified data".

  — [Foley, "AI Contracts in Health Care: Avoiding the Data Dumpster Fire"](https://www.foley.com/insights/publications/2025/06/ai-contracts-in-health-care-avoiding-the-data-dumpster-fire/)
- [INTL] **Ward and Smith (Mayukh Sircar, 23 June 2026), "Contract Architecture: Core AI Clauses for Vendor Agreements":**
  - "The default should be no training on customer data, prompts, inputs, and outputs." Where training is authorised: opt-in consent, segregation from other customers' data, de-identification standards and a **ban on re-identification**.
  - "Customer data and model interaction metadata should be elevated to confidential information with heightened protections."
  - Spell out how a data subject's deletion request will reach all personal data held by the AI tool.
  - Cross-border transfer mechanisms.
  - Customer ownership of inputs (and outputs, where appropriate).
  - Limits on the vendor's use of usage metadata.
  - Security commitments (encryption, least privilege, logging, monitoring) plus protection against model inversion, data extraction and adversarial attacks.
  - Breach-notice duties and who bears the costs, set out expressly.
  - Vendor must disclose whether the system is "high-risk" under applicable law and update that disclosure if it changes.
  - Model versioning and change-management commitments.
  - Ownership and post-termination treatment of models fine-tuned on customer data.
  - Right to terminate for breach, for untrustworthy performance, or if the system becomes high-risk.
  - Service credits and step-in rights for chronic failure.
  - "Mandate human review of AI outputs" before consequential decisions.
  - The article does **not** cover sub-processors, audit rights, specific breach-notice timelines or indemnity.
  - — [Ward and Smith, 23 Jun 2026](https://www.wardandsmith.com/article/contract-architecture-core-ai-clauses-for-vendor-agreements); [National Law Review reprint](https://natlawreview.com/article/contract-architecture-core-ai-clauses-vendor-agreements)
- [INTL] Separate strict no-training and deletion rights for customer content from the vendor's narrower rights to usage telemetry. — [Axiom, "AI Addendums"](https://www.axiomlaw.com/blog/ai-addendums-contract-clauses-to-negotiate-with-ai-vendors) (search summary)
- [INTL] **(June 2026)** Options when a vendor asks to train on customer data: prohibit outright, require opt-in consent, exclude sensitive data, or require anonymisation before training. — [Morgan Lewis, June 2026](https://www.morganlewis.com/fr/blogs/sourcingatmorganlewis/2026/06/key-considerations-when-allowing-a-vendor-to-train-its-ai-models-on-customer-data) (search summary)
- [INTL] Model clause: "Neither the model provider nor any integrated application provider may use customer data to develop or improve its services without explicit, written customer consent". — [Illinois ARDC "Implementing AI" guide](https://iardc.org/Files/Implementing-AI-Guide/inc/html/39.html) (search summary)
- [INTL] Example of vendor AI terms that bar AI **sub-processors** from training on customer data and require flow-down terms. — [AgencyBloc AI terms](https://www.agencybloc.com/about-us/terms-of-use/ai/) (search summary)
- [INTL] **(19 Nov 2026)** A customer-side AI rider can override a vendor's standard terms. — [Nixon Peabody, "Healthcare technology contracts"](https://www.nixonpeabody.com/insights/videos/2026/11/19/healthcare-technology-contracts) (search summary)
- [INTL] **OpenAI enterprise and API privacy commitments (page updated 8 Jan 2026):**
  - "We do not use your business data for training our models" (API data since 1 Mar 2023; opt-in only).
  - "OpenAI may securely retain API inputs and outputs for up to 30 days to provide the services and to identify abuse."
  - ZDR is available "for eligible endpoints if you have a qualifying use-case".
  - Customers own inputs and outputs; fine-tuned models are not shared.
  - BAAs are available for the API on request; AES-256 at rest, TLS 1.2+ in transit; SOC 2 Type 2; a DPA is available.
  - **Data residency and the sub-processor list are not stated on the page.**

  — [OpenAI Enterprise Privacy](https://openai.com/enterprise-privacy/)
- [INTL] OpenAI's healthcare addendum works as a BAA and prevails over the main agreement on its subject matter. — [OpenAI Healthcare Addendum PDF](https://cdn.openai.com/osa/healthcare-addendum.pdf) (search summary)
- [INTL] **PhysioNet (24 Sep 2025).** The credentialed Data Use Agreement for MIMIC (de-identified ICU data) "explicitly prohibits sharing access to the data with third parties", including "sending it through APIs or using it on online platforms". Locally deployed LLMs are the strongest recommendation. Cloud services must offer **zero data retention, no use for model training, and no human review**, and "if practices are unclear… do not use the service". Even claimed ZDR may be insufficient because of "internal processing, logging, or caching". Platform policies change without notice and should be reviewed regularly. — [PhysioNet, "Responsible use of MIMIC data with LLMs"](https://physionet.org/news/post/llm-responsible-use/)
- [INTL] ZDR is distinct from a no-training commitment and covers only the vendor side of an integration, so both must be verified separately. — [CASRAI guide on ZDR AI tools](https://casrai.org/guides/zero-data-retention-ai-tools-research) (search summary)
- [INTL] An academic-medical-centre AI governance handbook advises that restricted data should not leave the institutional network boundary without specific governance approval, and notes that some institutions still classify de-identified data as restricted. — [AMC AI Governance, "Data Access and Governance"](https://seandavi.github.io/amc-ai-governance/data.html) (search summary)
- [INTL] **Baseline processor clauses (GDPR Art. 28(3)), widely reused as a DPA template:**
  - process only on documented instructions;
  - confidentiality of personnel;
  - security measures;
  - sub-processors only with prior authorisation and with the same obligations flowed down;
  - assist with data-subject rights, breach handling and DPIAs;
  - delete or return all data at the end of services;
  - make available all information needed to demonstrate compliance and allow audits and inspections.

  — [GDPR Art. 28](https://gdpr-info.eu/art-28-gdpr/) (regulation text; not re-fetched in this session)
- [QATAR] The PDPPL guidelines require controllers to do processor due diligence and to have "adequate contracts" governing processing. — [Clyde & Co, Mar 2021](https://www.clydeco.com/en/insights/2021/03/new-regulatory-guidelines-on-the-qatar-persona-1)
- [QATAR] HMC's own notice commits to storage "in Qatar or in other countries that have adequate data protection laws". A vendor contract would have to respect that. — [HMC Privacy Notice](https://hamad.qa/EN/Patient-Information/Patient-Family-Rights/Pages/HMC-Privacy-Notice.aspx)

### Inferences
A gateway AI-vendor DPA checklist built from these sources:
1. **Purpose limitation**: process only to return the diagnostic or other output for this hospital.
2. **No training, fine-tuning, evaluation or product improvement** on inputs or outputs, including in de-identified or aggregated form, without written opt-in.
3. **Zero data retention** (or a stated maximum, e.g., 0 days, with abuse-monitoring logging waived) and **no human review** of payloads.
4. A **sub-processor list** with prior notice, a right to object, and flow-down of no-training and no-retention terms.
5. **Processing location** named (Qatar, or an approved adequate country) and no onward transfer.
6. **Audit rights** plus annual third-party attestation (SOC 2 / ISO 27001).
7. **Breach notice** fast enough for the hospital to meet the 72-hour PDPPL guideline window. The 24–48 hour figure is an inference from that window, not a cited standard.
8. **Deletion certificate** at termination and no surviving rights over any derived model.
9. **Model-change notice**: advance notice of model or version changes, since they trigger re-certification in the gateway's offline loop.
10. Liability cap tiered by clinical risk, and indemnities for privacy breaches.

The PhysioNet position supports the gateway design choice that **only gateway-minimised data ever reaches an outside API**, and that local models are preferred where feasible.

### Gaps
- No Qatar- or GCC-specific model AI DPA or MoPH procurement clause set was found.
- None of the law-firm sources fetched (Foley, Ward and Smith) gives specific **sub-processor, audit-rights or breach-notice-timeline** clause language. Those items rest on GDPR Art. 28(3) as a template and on inference from the PDPPL 72-hour window.
- Anthropic, Azure OpenAI and Google Vertex data-retention terms were not verified from primary pages in this session.

---

## 4. Insurer relationships: minimum-necessary claim data, how claims are exchanged in Qatar, SEHA 2013–2015, bans on using health data for underwriting

### Takeaway
Qatar's claims landscape went from SEHA to nothing to the current scheme:
- **SEHA (2013–2015)**: state insurer NHIC, a third-party administrator (TPA) handling provider claims, and a national claims data standard (IDS v5.x, approved by QNCC).
- **Suspension at end of 2015.**
- **Law No. 22 of 2021** (in force 2022): mandatory private insurance for expatriates and visitors, with insurers, TPAs, brokers and providers registered on an MoPH electronic platform.

The 2022 executive regulations require **express written member consent to disclose medical records** and impose confidentiality duties on insurers, claims managers and employers. No Qatari ban on using health data for underwriting was found. International comparators (US GINA/ACA, EU EHDS Art. 54) do ban it in specific forms.

### Cited Findings
**Qatar: SEHA (older, 2013–2015)**
- [QATAR] SEHA launched in phases from July 2013. Stage 1 covered Qatari women aged 12 and over for gynaecology and maternity care. It was managed by the state-owned National Health Insurance Company (NHIC), "with a Third-Party Administrator (TPA) contracted to manage provider claims". — [BMC Health Services Research 2015 abstract](https://link.springer.com/article/10.1186/1472-6963-15-S2-A6) (search summary)
- [QATAR] SEHA paid about QAR 1.3 billion (US$357m) in the 15 months from August 2013. A former acting NHIC CEO described "a detailed and manual audit… for all the claims… as well as checking of medical files". The scheme was suspended from 31 December 2015 by Cabinet decision, and the NHIC was liquidated. — [LaingBuisson IMTJ](https://www.laingbuissonnews.com/imtj/sudden-closure-of-qatari-national-health-insurance-scheme/); [Zawya, "SEHA: a critical eulogy"](https://www.zawya.com/en/business/seha-a-critical-eulogy-iwu97kzg); [Mondaq](https://webiis08.mondaq.com/insurance-laws-and-products/459026/qatars-mandatory-health-insurance-suspended) (search summaries)
- [QATAR] **(SEHA era)** The QNHI Data Management document says the **Insurance Data Set (IDS v5.x), approved by QNCC, must be used as the National Standard for claims submission and remittance**, and that brokers and consulting firms "are not permitted to process or submit claims on behalf of payors, healthcare providers or members". — [QNHI Data Management (MoPH QHIS)](https://qhis.moph.gov.qa/documents/76932/124581/QNHI-DATA-MANAGEMENT-ENG.pdf) (search snippet only; direct fetch was blocked by the site firewall. Whether this standard still applies after 2022 is unknown)

**Qatar: current scheme (Law No. 22 of 2021)**
- [QATAR] Law No. 22 of 2021 regulating health services was published 4 Nov 2021 and came into partial effect in May 2022. Non-Qatari residents and visitors must hold private insurance; Qatari citizens keep free care at government facilities. Employers must enrol employees and families with MoPH-registered insurers, and coverage is a prerequisite for residence permits. — [US ITA Market Intelligence, page dated 19 Nov 2026](https://www.trade.gov/market-intelligence/qatar-new-healthcare-insurance-law); [WTW, Dec 2021](https://www.wtwco.com/en-BE/Insights/2021/12/qatar-health-insurance-mandate-for-foreigners-becomes-law)
- [QATAR] The executive regulations (Minister of Public Health Resolution No. 8 of 2022) were published 1 Sep 2022 and effective 2 Sep 2022. They require "express written consent from each member to disclose their medical records". Confidentiality duties apply to insurers, brokers, claims management companies, employers and other entities. Reinsurance disclosures need express written permission. Clyde & Co note that the consent mechanism is not specified and that PDPPL may apply. — [Clyde & Co, 30 Sep 2022](https://www.clydeco.com/en/insights/2022/09/qatar-issues-executive-regulations-to-the-new)
- [QATAR] Insurers, TPAs, brokers and service providers must be registered on an MoPH electronic platform. Claims management companies manage claims under claims-management rules and assess reimbursable expenses. — [Clyde & Co, Dec 2021](https://www.clydeco.com/en/insights/2021/12/new-mandatory-health-insurance-system-introduced-i); [Oxford Business Group 2022](https://oxfordbusinessgroup.com/reports/qatar/2022-report/economy/universal-coverage-new-regulations-mandate-employer-sponsored-private-health-insurance-for-expatriates-and-foreign-tourists) (search summaries)
- [QATAR] HMC's privacy notice lists insurers among recipients of personal information as "parties involved in your care". — [HMC Privacy Notice](https://hamad.qa/EN/Patient-Information/Patient-Family-Rights/Pages/HMC-Privacy-Notice.aspx)

**International: minimum necessary and underwriting bans**
- [INTL] **Minimum necessary.** Caldicott Principle 3, "Use the minimum necessary confidential information", requires each item to be justified. — [GOV.UK Caldicott Principles](https://www.gov.uk/government/publications/the-caldicott-principles)
- [INTL] HIPAA's minimum-necessary standard applies to disclosures for payment, including claims to health plans, but not to disclosures for treatment. — [HHS minimum necessary guidance](https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/minimum-necessary-requirement/index.html) (not re-fetched in this session)
- [INTL] **US GINA Title I** prohibits group and individual health insurers from using genetic information to set eligibility or premiums, and from requiring genetic tests. Under the **ACA**, plans may not exclude coverage for pre-existing conditions. Insurers may still act on a manifested disease in some group-pricing contexts. — [DOL GINA compliance guide](https://www.dol.gov/sites/dolgov/files/EBSA/about-ebsa/our-activities/resource-center/publications/genetic-information-nondiscrimination-act-compliance-guide.pdf); [CRS R41314](https://www.everycrsreport.com/reports/R41314.html); [Jackson Laboratory GINA overview](https://www.jax.org/education-and-learning/clinical-and-continuing-education/clinical-topics/gina-overview) (search summaries)
- [INTL] **EU European Health Data Space (Regulation (EU) 2025/327; adopted 11 Feb 2025, in force 26 Mar 2025).** Article 54 prohibits secondary use of health data for decisions detrimental to a person or group, for marketing, and for decisions on insurance or credit contracts (e.g., changing premiums) that discriminate against people based on their health data. — [European Commission: Reuse of health data](https://health.ec.europa.eu/ehealth-digital-health-and-care/reuse-health-data_en); [Taylor Wessing](https://www.taylorwessing.com/de/global-data-hub/2025/eu-digital-laws-and-gdpr/gdh---european-health-data-space-and-the-gdpr); [Streamlex EHDS Art. 54](https://streamlex.eu/articles/ehds-en-art-54/) (summaries; check exact wording in the Official Journal)

### Inferences
- The gateway's insurer channel ("structured claim only") matches both Qatari practice and international norms. Claims historically moved in a **structured national dataset** (IDS v5.x) through a TPA, not as free-text notes. The 2022 regulations make disclosing medical records to insurers **consent-based**.
- A defensible policy clause: release to an insurer only the coded claim fields (member ID, encounter, ICD and procedure codes, charges) needed to adjudicate. Free-text notes are released only on a specific written member authorisation tied to a claim query. The insurer's use is restricted contractually to adjudication, fraud control and audit. Underwriting, pricing and eligibility decisions are prohibited, by analogy with EHDS Art. 54, GINA and the ACA.
- Nationality matters here too: Qatari citizens are generally outside the mandatory private scheme, so an insurer channel would mostly carry expatriate and visitor claims.

### Gaps
- The current (post-2022) Qatari e-claims technical standard was not found. Unknown: whether IDS v5.x or an MoPH platform-specific format applies, and what the coding standard is (e.g., ICD-10-AM/ACHI vs ICD-10-CM/CPT).
- No Qatari provision banning use of health data for underwriting or pre-existing-condition exclusion was found. Law 22's text on this was not retrieved.
- The name of SEHA's TPA was not confirmed.

---

## 5. Public-health reporting: separating identified notifiable-disease reports from aggregate statistical extracts; statistical disclosure control practice

### Takeaway
In Qatar, identified notifiable-disease reports go to MoPH through a dedicated legal channel, the **SAVES** electronic surveillance system, under a statutory duty on every practitioner and laboratory. Statistical outputs are a separate, aggregate stream. UK public bodies show that small-cell protection is moving from **blanket suppression below 5** to **risk-based rules, rounding to the nearest 5, and secondary suppression**.

### Cited Findings
- [QATAR] Ahead of the 2021 Arab Cup and 2022 World Cup, MoPH built the **Surveillance and Vaccination Electronic System (SAVES)**. It is one platform where facilities, hospitals and laboratories notify infectious diseases, with vaccine records and daily or weekly trend reports. Implementation began in early 2020. Qatar "mandated by law that every healthcare practitioner and laboratory should report infectious diseases". — [BMC Public Health 2024, "Enhancing the notification system…"](https://link.springer.com/10.1186/s12889-024-18016-9)
- [QATAR] **(2022)** MoPH's Notification Enhancement Project proposed a shorter notifiable-disease list, training for health workers, and **focal points in every healthcare facility**, and significantly improved notification rates. — [BMC Public Health 2024](https://bmcpublichealth.biomedcentral.com/counter/pdf/10.1186/s12889-024-18016-9.pdf)
- [QATAR] **(older, 2020)** In primary health centres, electronic reporting produced about twice as many notifications as paper for 23 notifiable diseases. 100% of electronic notifications were timely, against 28% on paper. — [BMJ Innovations](https://innovations.bmj.com/content/early/2020/01/14/bmjinnov-2018-000329.full)
- [QATAR] HMC's privacy notice lists "public health surveillance" and "population health management" as lawful purposes for processing, separate from consent-based release. — [HMC Privacy Notice](https://hamad.qa/EN/Patient-Information/Patient-Family-Rights/Pages/HMC-Privacy-Notice.aspx)
- [INTL] The Royal College of Paediatrics and Child Health (RCPCH) replaced its "Small Numbers Policy", which "advised a blanket suppression of any result linked to fewer than five individuals", with risk-based guidance for reports and dashboards. — [RCPCH guidance](https://www.rcpch.ac.uk/resources/managing-data-disclosure-risks-public-reports-dashboards-rcpch-guidance)
- [INTL] Hospital Episode Statistics (HES) and the Emergency Care Data Set (ECDS) used to replace counts of 1–5 with "*" and apply secondary suppression. Current rules round sub-national counts **to the nearest 5**, leave England totals unrounded, and no longer need secondary suppression. — [NHS Digital HES/ECDS disclosure control methodology (mirror)](https://nhsd-proxy.openprescribing.net/data-and-information/data-tools-and-services/data-services/hospital-episode-statistics/disclosure-control-methodology-for-hospital-episode-statistics-and-emergency-care-data-set) (search summary)
- [INTL] ONS suppresses very small numbers ("usually numbers less than three") in birth and death tables. — [ONS policy on protecting confidentiality in birth and death tables](https://www.ons.gov.uk/methodology/methodologytopicsandstatisticalconcepts/disclosurecontrol/policyonprotectingconfidentialityintablesofbirthanddeathstatistics) (search summary)
- [INTL] UKHSA replaces small numbers with "[c]" and applies secondary suppression so hidden cells cannot be recovered from totals. — [UKHSA data management in official statistics policy](https://www.gov.uk/government/publications/ukhsa-official-statistics-compliance-documents/data-management-in-official-statistics-policy) (search summary)
- [INTL] NHS Business Services Authority (NHSBSA): suppression and rounding are "determined on a case by case risk basis". An NHS England risk assessment for cancer waiting-times data concluded no small-number suppression was needed. — [NHSBSA SDC protocol](https://www.nhsbsa.nhs.uk/sites/default/files/2020-10/nhsbsa-sdc-protocol.pdf); [NHS England Risk of Disclosure: CWT (Sep 2025)](https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2025/09/Risk-of-Disclosure-CWT-publication.pdf) (search summaries)
- [INTL] The UK Government Analysis Function publishes cross-government SDC guidance for tables produced from administrative data. — [Analysis Function: SDC for tables from administrative data](https://analysisfunction.civilservice.gov.uk/policy-store/sdc-for-tables-produced-from-administrative-data/)

### Inferences
- The gateway's "MoPH reporting" channel should be split in policy into two flows:
  - **(a) Statutory notifiable-disease reports**: identified, sent through SAVES, outside the de-identification gateway, under the legal duty. The gateway only logs the event.
  - **(b) Aggregate statistical extracts**: de-identified, with small-cell suppression or rounding plus secondary suppression. Thresholds should be **set by risk assessment**, not fixed at <5 by default, with a stricter setting for small nationality groups.
- Nationality-by-diagnosis cross-tabs in Qatar are high risk, because some nationality groups are very small. RCPCH and NHSBSA's move to risk-based SDC supports a rule that small-population cells always trigger review.

### Gaps
- No Qatar MoPH statistical disclosure control policy or small-cell threshold was found.
- The current official notifiable-disease list and the exact statute (believed to be Decree-Law No. 17 of 1990 on prevention of communicable diseases) were not verified in this session.
- No source was found describing how HMC internally separates SAVES reporting from research or statistical extracts.

---

## 6. Evidence on automation bias and meaningful human oversight in clinical AI

### Takeaway
Experimental evidence shows clinicians follow wrong AI suggestions at large cost to accuracy:
- In mammography, accuracy fell from about 80% to 20–46% when the AI was wrong (Dratsch 2023).
- In hospital diagnosis, a systematically biased model cut accuracy by 11 points, and explanations did not fix it (Jabbour 2023).

Experience reduces automation bias but does not remove it. Supported mitigations are user accountability, training on the system's reasoning and limits, design choices (where advice appears, confidence display), and lower workload and time pressure. A "human in the loop" who sees the AI answer first, under time pressure, with no accountability, is likely to rubber-stamp.

### Cited Findings
- [INTL] **(older, 2012)** Goddard, Roudsari and Wyatt's systematic review (JAMIA 19(1):121) included 74 of 13,821 papers.
  - Factors that made automation bias more or less likely: user cognitive style, experience with decision support systems and with the task, trust and confidence; and in the environment, workload, task complexity and time constraint.
  - Mitigations: training, "emphasizing user accountability", where the advice appears, and updated confidence levels on decision-support output.
  - — [JAMIA 2012](https://academic.oup.com/jamia/article/19/1/121/732254); [PMC3240751](https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751)
- [INTL] **(older, ~2020)** A later review notes that most automation-bias research comes from human-factors studies, which assume it happens mainly in multitasking settings, and tests that assumption against the healthcare literature. This matters for whether single-task reviewers also need safeguards. — [PMC7651899](https://pmc.ncbi.nlm.nih.gov/articles/PMC7651899) (search summary)
- [INTL] **Dratsch et al., *Radiology*, 2 May 2023 (DOI 10.1148/radiol.222176).** Purported AI BI-RADS suggestions were wrong in 12 of 40 mammograms. Inexperienced readers' accuracy fell from 79.7% (correct AI) to 19.8% (incorrect AI). Very experienced readers fell from 82.3% to 45.5%. The authors recommend making users "feel accountable for their own decisions" and teaching them about the system's reasoning. — [RSNA news](https://www.rsna.org/news/2023/may/ai-bias-may-impair-accuracy); [University of Lübeck record](https://research.uni-luebeck.de/en/publications/automation-bias-in-mammography-the-impact-of-artificial-intellige/)
- [INTL] **Jabbour et al., *JAMA*, 19 Dec 2023 (DOI 10.1001/jama.2023.22295).** A randomised vignette study of 457 hospitalist physicians, NPs and PAs in 13 states:
  - Baseline accuracy was about 73%.
  - A standard AI model raised accuracy by 2.9 points, or 4.4 points with explanations.
  - A **systematically biased** model lowered it by 11.3 points, and still by 9.1 points with image-based explanations.
  - "AI model explanations did not help clinicians recognize systematically biased AI models."

  — [University of Michigan IHPI](https://ihpi.umich.edu/news-events/news/clinicians-could-be-fooled-biased-ai-despite-explanations); [PMC10731487](https://pmc.ncbi.nlm.nih.gov/articles/PMC10731487); [MDedge summary](https://mdedge.com/content/systemic-bias-ai-models-may-undermine-diagnostic-accuracy) (sources differ slightly on the exact figure for biased model + explanation)
- [INTL] **(2026)** A JMIR systematic review of AI decision support in primary care finds "an important gap between the rapid development of AI-CDSSs and the lack of robust, comparable evidence" for reliable use. — [JMIR 2026](https://www.jmir.org/2026/1/e96882/PDF) (search summary)
- [INTL] The EU AI Act makes awareness of automation bias an explicit part of the oversight duty for high-risk systems, together with override and "stop" powers (Art. 14(4)(b), (d), (e)). — [AI Act Art. 14](https://artificialintelligenceact.eu/article/14/)
- [INTL] Ben Green (2022) argues that policies requiring human oversight of government algorithms often fail, because people are poor at judging algorithm quality and correcting errors, and that such policies can lend false legitimacy to flawed systems. — [Green, "The flaws of policies requiring human oversight of government algorithms," *Computer Law & Security Review* 45 (2022)](https://doi.org/10.1016/j.clsr.2022.105681) (not re-fetched in this session)
- [INTL] Commentary on Sidra and Qatar AI diagnostics argues that "clinical oversight must remain central to every deployment" (opinion, not policy). — [The Peninsula editorial, 22 Jul 2026](https://thepeninsulaqatar.com/editorial/22/07/2026/ai-driven-diagnostics-in-qatar)

### Inferences
Design features that make the gateway's human checkpoint meaningful, each tied to the evidence above:
1. **Risk-based routing instead of reviewing everything**, so reviewers are not overloaded. Workload and time pressure drive automation bias (Goddard).
2. **Independent judgement first** where feasible, e.g., the reviewer flags risks before seeing the agent's proposed redaction, or the reviewer's view is not pre-filled with the system's answer. This draws on advice-placement findings.
3. **Named accountability**: each decision is signed and logged with a reason. Accountability is the mitigation that appears most consistently across the studies (Goddard, Dratsch).
4. **Seeded test cases**: inject known-bad outputs at a low rate, as Dratsch did with 12 of 40 cases, to measure whether reviewers catch errors. Track override and agreement rates; near-100% agreement is a warning sign.
5. **Do not rely on explanations alone** (Jabbour). Give reviewers concrete evidence instead: the leaked span, the re-identification test result.
6. **Authority to stop or override**, plus escalation from clinician to DPO or Guardian for loosening requests (AI Act Art. 14).
7. Every human change goes back through the fixed rule checks. This guards against human error as well as machine error, and answers Green's critique that oversight alone is insufficient.

### Gaps
- No study specific to automation bias in **de-identification or privacy review** tasks (as opposed to diagnosis) was found. The evidence is extrapolated from diagnostic decision support.
- No Qatari or Gulf study on clinician automation bias was found.
- Lyell & Coiera (2017) and other verification-complexity studies were not retrieved in this session.
