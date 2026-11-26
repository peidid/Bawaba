# Qatar PDPPL (Law No. 13 of 2016) and Official Guidance: Article-Level Reference for a Hospital Sharing Patient Data with an AI Vendor, Insurers and MoPH

Research date: 22 November 2026. Scope: Qatar onshore law only. The Qatar Financial Centre (QFC) has its own Data Protection Regulations, run by the QFC Data Protection Office. They apply only to QFC-licensed entities and are not covered here ([Chambers 2026, s.1.1](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice)).

**Source note (read first).**
- **Law text.** Article text below comes from the unofficial English translation by the regulator's Compliance and Data Protection (CDP) Department ("Law No.13 of 2016 Personal Data Privacy Protection – Compliance and Data Protection Department"), hosted by the UNIDIR Cyber Policy Portal ([PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf); old link database.cyberpolicyportal.org/api/files/1676833786171f3yskpqxl38.pdf).
  - Every page carries this disclaimer: "This document is not official and the official version of the law is the one published in the Official Gazette number 15 of year 2016 that is available on almeezan.qa".
  - The official Arabic and English text is on Al Meezan ([LawPage id=7121](https://www.almeezan.qa/LawPage.aspx?id=7121&language=en)). That page renders by script and could not be read by the fetch tool.
  - The law was issued at the Emiri Diwan on 03/02/1438 AH, which is **3 November 2016**.
- **Two translations.** NCSA guidelines quote a slightly different official translation. For example, Art. 13 reads "adopt all necessary precautions…" in the guidelines. Where wording differs, both are noted.
- **Gaps in the PDF text.** A few fragments did not come through when the text was extracted from the PDF. They are marked [fragment missing]. Text in [square brackets] is reconstructed and must be checked against Al Meezan before it is quoted.

---

## 1. Definitions and scope (Arts. 1–2); de-identified, anonymised and pseudonymised data

### Takeaway
The PDPPL defines personal data broadly. Data counts if the person "can be reasonably defined", including by combining it with other data. So pseudonymised (key-coded) patient data is very likely still personal data. The law itself says nothing about anonymisation. Secondary sources and NCSA-hosted material treat truly anonymised, irreversible data (for example aggregated outcomes) as outside the law. Pseudonymisation is treated as a safeguard, not as a way out of the law.

### Cited Findings
- **Art. 1, definitions** (CDP translation, [UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf)):
  - **Ministry:** "Ministry of Transport and Communications". **Minister:** "Minister of Transport and Communication".
  - **Competent Department:** "the competent administrative unit at the Ministry".
  - **Competent Authority:** "any government entity competent, as per law, to regulate acts or procedures pertinent to Personal Data Processing and supervision of the same".
  - **Individual** (the data subject): "a natural person whose Personal Data are processed".
  - **Controller:** "a natural or legal person who, whether acting individually or jointly with others, determines how Personal Data may be processed and determines the purpose(s) of any such processing".
  - **Processor:** "a natural or legal person who processes Personal Data for the Controller".
  - **Personal Data:** "data of an individual whose identity is defined or can be reasonably defined whether through such Personal Data or through the combination of such data with any other data".
  - **Personal Data Processing:** "Personal Data Processing through one operation or more such as gathering, receipt, registration, organization, storage, preparation, modification, retrieval, usage, disclosure, publication, transfer, withholding, destruction, erasure and cancellation".
  - **Cross-Border Data Flows:** "access, watch, retrieve, use or store [Personal Data without restriction of State borders]". The second half is a missing fragment. DLA Piper paraphrases it as "without regard to state borders" ([DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=law&c=QA)).
  - **Lawful Purpose:** "The purpose for which Personal Data of an Individual is processed, in accordance with the law".
  - **Acceptable Practices:** "processing activities determined or approved by the Competent Department with regard to various types of Lawful Purposes".
  - **Direct Marketing:** "sending any advertising or marketing material, in whatsoever means, to certain individuals".
  - **Website Operator:** defined as someone who operates a website and "gathers or processes Personal Data of users or visitors".
- **Art. 2, material scope.** The law applies to personal data "when it is electronically processed, or obtained, gathered or extracted in preparation in any other way for electronic processing, or when processed via a combination of electronic and traditional processing". It does not apply to processing "by individuals within a private or a family scope", or to processing "for the purpose of obtaining official statistical data as per provisions of … law No (2) of 2011" (the Official Statistics law) ([UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf)).
- **Controller and processor roles in the NCSA guideline.** An organisation is:
  - a **controller** "if it is the main decision-maker exercising overall control over why and how personal data is processed";
  - a **processor** "if it is following the instructions of a Controller or is processing personal data on their behalf";
  - a **joint controller** "if it jointly makes decisions or exercises shared control over why and how the personal data is processed with another controller".
  - Source: [NCSA Controller and Processor Guideline PDPPL-02050209E, v2.0, Sept 2022](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/2904/1.0~ec44b72b-0d7a-4559-8889-2101cb82a698?mimetype=application%2Fpdf&filename=1.pdf).
- **Anonymisation in the law.** The PDPPL does not expressly regulate anonymised data. Data that no longer allows identification "would fall outside the scope of the PDPPL". The law does not address pseudonymised data ([Chambers 2026, GLA & Company, s.1.4](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice)).
- **NCSA-hosted health deck.** The deck was presented by PwC at NCSA's International Data Privacy Day event, January 2026, and is hosted in NCSA's document library. It is not formal guidance.
  - It lists "Hospital shares aggregated anonymized treatment outcomes with its research unit" as an example of **non-personal** data processing.
  - Its definitions: anonymised = "the individual can no longer be identified, and the process is effectively irreversible"; pseudonymised = "re-identification is possible".
  - Its advice: "Prefer anonymized datasets … where research does not require re-identification; where follow-up is needed, use pseudonymization … with strong technical and organizational controls so that only the originating institution can reconnect codes to patients."
  - For secondary use, such as training a predictive risk model on treatment data: "Apply data minimization and de-identification (use only what is needed; pseudonymize where possible – or anonymize)".
  - Source: [NCSA/PwC, "Data Privacy in Medical Research", Jan 2026](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/10207/1.0~fc4efdb1-0710-4db9-a751-c48e068c9509?mimetype=application%2Fpdf&filename=Presentation+-+Data+Privacy+in+Medical+Research+-+IDPD+2026+%282%29.pdf).
- **NCSA Advisory Note (Oct 2025).** It lists "anonymization" among "Enhanced Security Measures" for special-nature data, next to encryption and access controls ([NCSA PDPPD Advisory Note PDPPL-202501AN(E), Oct 2025](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/9737/1.0~b83017e6-db74-4592-a981-caae6512cbf8?mimetype=application%2Fpdf&filename=Advisory+Note+on+Building+a+Comprehensive+Data+Privacy+Program_EN_Final.pdf)).

### Inferences
- **Pseudonymised data is in scope.** The Art. 1 test is "can be reasonably defined … through the combination of such data with any other data". Key-coded or pseudonymised clinical notes sent to an AI vendor are therefore almost certainly personal data, and health data of a special nature (Art. 16), especially where the hospital keeps the key. The full PDPPL then applies, including the Art. 16 permit.
- **Anonymised data may fall outside.** Only data that is irreversibly anonymised against "reasonably" available means can plausibly be treated as outside the law. Free-text clinical notes are hard to anonymise fully. The governance lead should document a re-identification risk assessment before treating any dataset as anonymous.
- **Paper records.** Art. 2 limits scope to electronic processing (or processing in preparation for it). Purely paper records not destined for digitisation fall outside, but a modern hospital EHR environment is fully in scope.
- **Official statistics.** The exclusion covers only official statistics under Law No. 2 of 2011. Routine statistical reporting by a hospital is not excluded on that basis alone.

### Gaps
- No statutory definition of "anonymisation" or "pseudonymisation" was found. I did not obtain the text of NCSA's "Principles of Data Privacy" guideline (PDPPL-02050201E) to check whether it defines either term.
- I could not render the official Al Meezan English or Arabic text. The tail of the cross-border definition is reconstructed.

---

## 2. Data subject rights (Arts. 3–7, 9, 20–21)

### Takeaway
The law gives individuals a general right to fair and dignified processing (Art. 3). It lets them withdraw consent, object, request erasure and request correction (Art. 5). It also gives a right of access with notification of processing and a copy (Art. 6), and a right to prior notice of controller details and purposes (Art. 9). The law sets no response deadline. NCSA guidance sets 30 days.

### Cited Findings
All article text from the [UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf) unless another source is given.

- **Art. 3, general principle.** "Each Individual has the right to the protection of the Personal Data thereof that shall be processed only within the framework of transparency, honesty, and respect of human dignity, and acceptable practices".
- **Art. 4, consent or lawful purpose.** "The Controller shall process Personal Data only after obtaining the consent of the Individual, unless data processing is necessary to achieve a Lawful Purpose for the Controller or the other recipient of such data."
- **Art. 5, rights the individual may use "at any time":**
  1. "Withdraw the prior consent thereof for Personal Data Processing."
  2. "Object to processing … if such processing is not necessary to achieve the purposes for which such Personal Data have been collected or where such collected Personal Data are beyond the extent required, discriminatory, unfair or illegal."
  3. Request "omission or erasure" in the cases in items 1–2, "upon cessation of the purpose for which the processing has been conducted, or where all justifications for maintaining such Personal Data by the Controller cease to exist".
  4. "Request corrections … A request so made shall be accompanied with proof of the accuracy of such request."
- **Art. 6, access.** An individual may "at any time, access the Personal Data thereof and apply to review the same" and has the right to:
  1. "Be notified of processing the Personal Data thereof and the purposes for which such processing is conducted."
  2. "Be notified of any disclosure of inaccurate Personal Data."
  3. "Obtain a copy of the Personal Data thereof after paying an amount that shall not exceed the service charge."
- **Art. 7, procedures.** The procedures for requests under Arts. 5–6 "shall be specified by a decision of the Minister". The opening words of the article are a missing fragment.
- **Art. 9, prior notice.** Before starting processing, the controller must inform the individual of:
  1. [the details of the Controller or any other party processing the data] "for the Controller or to be used thereby" (partial fragment);
  2. "The Lawful Purposes";
  3. a "Comprehensive and accurate description of the processing activities and the levels of disclosure"; if the controller fails to do so, "a general description thereof";
  4. "Any other information that is necessary".
- **Arts. 20–21, limits on access.**
  - Art. 20: the controller need not give reasons for refusing an Art. 6 request if disclosure would defeat Art. 18 purposes (security, crime and similar).
  - Art. 21: the controller is exempt from Art. 6 where disclosure would "cause harm to commercial interests of another individual". It is also exempt where disclosure would reveal another individual's data without consent and "may lead to physical or moral damage".
- **NCSA Individuals' Rights Guidelines (April 2026 coverage).** These map the rights as follows: protection (Art. 3), withdrawal of consent (Art. 5/1), objection (Art. 5/2), erasure (Art. 5/3), correction (Art. 5/4), and access, notification of processing and notification of inaccurate disclosure (Art. 6).
  - "Controllers must respond to erasure requests within 30 days."
  - Controllers must notify third parties the data was shared with and explain any rejection.
  - On objection, controllers must "provide human review for automated decisions".
  - On access, controllers must explain data categories, purposes, retention periods, sharing and processing location.
  - Source: [The Peninsula, 18 Apr 2026](https://www.thepeninsulaqatar.com/article/18/04/2026/explainer-ncsa-issues-guidelines-on-individuals-personal-data-privacy-protection-law-in-qatar).
- **2020 guidelines.** These required policies and procedures for rights requests and responses "within 30 days" ([Clyde & Co, 15 Mar 2021](https://www.clydeco.com/en/insights/2021/03/new-regulatory-guidelines-on-the-qatar-persona-1)).
- **Privacy notice content (Advisory Note, Oct 2025):**
  - controller identity and contact details;
  - Data Privacy Office/Officer contact details, if one exists;
  - what data is processed, "highlighting where such data is of a special nature";
  - how data is collected;
  - permitted reasons for collection and for disclosure to other parties;
  - retention period and security;
  - individuals' rights and the right to complain to the PDPPD;
  - "Details of any cross-border data disclosures" and "Details of any automated decision-making including profiling".
  - Where consent is the basis, "explicit consent should be obtained … by presenting the Data Privacy Notice".
  - Source: [NCSA Advisory Note, Oct 2025](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/9737/1.0~b83017e6-db74-4592-a981-caae6512cbf8?mimetype=application%2Fpdf&filename=Advisory+Note+on+Building+a+Comprehensive+Data+Privacy+Program_EN_Final.pdf).
- **Complaints (Art. 26).** An individual may complain to the Competent Department about violations ([UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf)). In 2026, NCSA said complaints go to the "Personal Data Privacy Protection Administration" ([The Peninsula, 10 Jun 2026](https://www.thepeninsulaqatar.com/article/10/06/2026/ncsa-highlights-key-role-of-pdppd-in-safeguarding-privacy-rights)).

### Inferences
- **What hospital policies must cover.** Policies should provide for: withdrawal, objection, erasure and correction (Art. 5); access, copy and notification (Art. 6); a 30-day response standard (guidance); fees capped at service cost (Art. 6(3)); and a pre-collection privacy notice (Art. 9) that names special-nature data, the AI vendor, insurers and MoPH as recipient categories, any cross-border flows, and any automated decision-making.
- **Rights are not portable.** The PDPPL has no data portability right, unlike the GDPR.

### Gaps
- I did not find any ministerial decision under Art. 7 setting request procedures.
- I did not obtain the full text of the NCSA Individuals' Rights Guideline (PDPPL-02050205E). The 30-day figure is reported through press coverage and Clyde & Co, not read directly.

---

## 3. Controller and processor duties (Arts. 8–14, 28)

### Takeaway
Controllers must:
- process honestly and lawfully;
- build privacy into product and system design;
- take administrative, technical and financial precautions;
- give notice;
- keep data relevant, accurate and no longer than needed;
- review privacy before new processing (the basis for DPIAs);
- run a Personal Data Management System;
- train staff;
- handle complaints and requests;
- audit;
- verify processors.

Processors share the security duty and must tell the controller "forthwith" about any breach. NCSA guidance turns these into a written contract requirement, records of processing (ROPA), DPIAs and privacy by design.

### Cited Findings
Article text from the [UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf) unless another source is given.

- **Art. 8, controller duties:**
  1. "Processing Personal Data honestly and legitimately."
  2. "Consider the controls related to designing, changing or developing products, systems and services pertinent to Personal Data Processing" (privacy by design).
  3. "Taking appropriate administrative, technical and financial precautions to protect Personal Data, in accordance with what is determined by the Competent Department."
  4. Follow "The privacy protecting policies developed by the Competent Department, and a decision thereon shall be issued by the Minister."
- **Art. 10, data quality.** Relevance and adequacy ("relevant to Lawful Purposes and adequate for achieving the same"); accuracy ("accurate, complete and up to date"); storage limitation ("shall not keep any Personal Data for a period of time that exceeds the necessary period").
- **Art. 11, required procedures:**
  1. "Reviewing privacy protection measures before proceeding with new processing operations."
  2. "Identifying Processors responsible for Personal Data protection."
  3. "Training and raising awareness of Processors on protecting personal data."
  4. "Developing internal systems to receive and investigate complaints, and data access and omission or correction requests; and they shall be made available to individuals."
  5. "Developing internal systems for the effective management of Personal Data, and reporting any breach of measures aiming at the protection thereof." The NCSA translation reads: "Develop and implement an internal effective Personal Data management system, and report any breach of protection measures thereof."
  6. "Using appropriate technologies to enable individuals to exercise their rights to directly access, review and correct their respective Personal Data."
  7. "Conducting comprehensive audits and reviews on the compliance extent with Personal Data protection requirements."
  8. In the NCSA translation: "Verify Processors' compliance with the instructions given thereto, adoption of appropriate precautions to protect Personal Data, and follow through on the same constantly."
  - Sources for the NCSA wording: [Breach Guideline](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/2991/1.0~5b70754f-6861-4223-8368-b0c74bd1a261?mimetype=application%2Fpdf&filename=BGJ.pdf) (item 5); [Controller and Processor Guideline](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/2904/1.0~ec44b72b-0d7a-4559-8889-2101cb82a698?mimetype=application%2Fpdf&filename=1.pdf) (item 8).
- **Art. 12, disclosure to processors.** When disclosing or transferring data to a processor, the controller must "take into consideration that it is in line with Lawful Purposes and is processed according to provisions hereof."
- **Art. 13, security (controller and processor).** "Each of the Controller and the Processor shall take the precautions necessary to protect Personal Data against loss, damage, change, disclosure, access thereto, or the inadvertent or illegal use thereof." Precautions must be "commensurate with the nature and the importance of the Personal Data". "The Processor shall forthwith notify the Controller of the existence of any breach of the precautions referred to, or where any risk arises threatening Personal Data in any way."
- **Art. 14, breach notification.** See section 6.
- **Art. 28, void contracts.** "Any contract or agreement made in violation of the provisions hereof shall be regarded as null and void."
- **Processor contracts (NCSA Controller and Processor Guideline, v2.0, Sept 2022).** "a written contract will need to be put in place" to meet Art. 11(8).
  - The contract must cover: "the subject matter and duration of the processing"; "the nature and purpose of the processing"; "the types of personal data being processed, and the categories of individuals"; and "the controller's duties and rights".
  - It must also contain specific provisions on: processing only on "the controller's documented instructions"; "appropriate security measures"; "the use of sub-processors"; "the duty of confidentiality"; individuals' rights; assistance to the controller; audit and review; and what happens to the data at the end of the contract (from the table of contents, ss.5.4–5.11).
  - The same contract terms apply between processors and sub-processors.
  - Due diligence is required: the controller should "develop the DPIA with the processor" or obtain the processor's information to complete one, and document its decision on whether the processor's precautions are adequate.
  - During processing the controller should monitor compliance and carry out audits. After processing it should tell the processor to stop and confirm that the processor "erases such data".
  - A **joint controller agreement** is expected where two organisations jointly decide purposes and means. The Advisory Note says "a joint controller agreement should be established and executed".
  - Sources: [C&P Guideline](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/2904/1.0~ec44b72b-0d7a-4559-8889-2101cb82a698?mimetype=application%2Fpdf&filename=1.pdf); [Advisory Note](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/9737/1.0~b83017e6-db74-4592-a981-caae6512cbf8?mimetype=application%2Fpdf&filename=Advisory+Note+on+Building+a+Comprehensive+Data+Privacy+Program_EN_Final.pdf).
- **Guideline expectations reported for the 2020 guidelines:**
  - a Personal Data Management System (PDMS);
  - a Record of Processing Activities (ROPA) that departments are trained to update;
  - DPIAs "before undertaking new processing activities", "particularly for prospective data exports or special nature data". The PDPPL itself does not expressly require DPIAs; they derive from Art. 11(1).
  - privacy by design and default;
  - enhanced due diligence on processors.
  - Source: [Clyde & Co, 15 Mar 2021](https://www.clydeco.com/en/insights/2021/03/new-regulatory-guidelines-on-the-qatar-persona-1).
- **When DPIAs are expected.** "Controllers should carry out DPIAs before carrying out new processing activities. They are particularly important where the processing may cause serious damage." Indicators of higher-risk processing:
  - "processing any special nature personal data";
  - "using a new innovative technology or an existing technology in a new way";
  - "automated decision-making which leads to a decision to limit an individual's access to a product, service, opportunity or benefit";
  - collecting data via third parties;
  - tracking or monitoring;
  - "undertaking a cross-border personal data transfer";
  - direct marketing;
  - marketing to children without parental consent;
  - processing new to the industry.
  - The guideline also ties DPIAs and the ROPA to "Articles 11(1) and 13".
  - Source: [NCSA Breach Guideline PDPPL-02050217E, v2.0, Sept 2022](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/2991/1.0~5b70754f-6861-4223-8368-b0c74bd1a261?mimetype=application%2Fpdf&filename=BGJ.pdf).
- **ROPA guideline (PDPPL-02050212E).** Controllers log the additional condition relied on for special-nature processing and link any permission obtained under Art. 16. This is reported from a search-result summary of the [NCSA ROPA Guideline](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/8878/1.0~2b2a468e-457e-4ea3-a609-b42546607d63?mimetype=application%2Fpdf&filename=Record+of+Processing+Activities+-+Guideline+for+Regulated+Entities+%284%29.pdf); I did not read the full text.
- **Data Privacy Office or Officer.** The law has no DPO requirement ([DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=law&c=QA)).
  - NCSA recommends a Data Privacy Office, either "a department of its own with a dedicated Data Privacy Officer or … a role within another appropriate department". The DPO should be able to "perform their duties and tasks in an independent manner".
  - NCSA also recommends an overarching internal data privacy policy, approved by top management, plus dedicated procedures for rights, breaches, "data retention and disposal" and "oversight of data processors".
  - Source: [Advisory Note, Oct 2025](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/9737/1.0~b83017e6-db74-4592-a981-caae6512cbf8?mimetype=application%2Fpdf&filename=Advisory+Note+on+Building+a+Comprehensive+Data+Privacy+Program_EN_Final.pdf).
- **NCSA tools named in the Advisory Note:** "Organization Level Privacy Compliance Assessment Tool", "Privacy by Design Assessment Tool", "Data Privacy Impact Assessment (DPIA) - Template for Regulated Entities", "Vendor Privacy Management Tool", and the "National Incident Management Framework" ([Advisory Note](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/9737/1.0~b83017e6-db74-4592-a981-caae6512cbf8?mimetype=application%2Fpdf&filename=Advisory+Note+on+Building+a+Comprehensive+Data+Privacy+Program_EN_Final.pdf)).

### Inferences
- **AI diagnostic vendor as processor.** If the vendor processes only on the hospital's instructions, it is a processor. The hospital must then: identify it (Art. 11(2)); review privacy before onboarding, i.e. a DPIA (Arts. 8(2), 11(1)); disclose only in line with lawful purposes (Art. 12); have a written contract with the NCSA-listed clauses; and verify and monitor it continuously (Art. 11(8)). The vendor carries its own Art. 13 security duty and must notify breaches "forthwith".
- **AI vendor as controller.** If the vendor reuses patient data to train or improve its own models for its own purposes, it likely becomes a controller or joint controller (C&P Guideline definitions). It then needs its own lawful basis and its own Art. 16 permit.
- **Insurers.** Insurers receiving claims data decide their own purposes, so they are most likely independent controllers. The hospital's disclosure to them is processing under Art. 1 that needs a basis under Art. 4 (consent or a Lawful Purpose).
- **Unlawful contract terms.** Under Art. 28, a vendor or data-sharing contract term that conflicts with the PDPPL is void. Examples would be unlimited vendor reuse rights or no breach notification duty.

### Gaps
- I found no ministerial decision under Art. 8(3)–(4) setting binding "precautions" or "privacy protecting policies". The guidelines say they should be read with "any related ministerial decisions", but name none.
- I did not obtain the full text of the DPIA guideline (PDPPL-02050206E), the Privacy by Design guideline (PDPPL-02050208E) or the PDMS guideline (PDPPL-02050203E).

---

## 4. Personal data of a special nature (Art. 16) and the permit procedure

### Takeaway
Health data, and data on physical or psychological condition, is "Personal data with special nature". It may be processed only after obtaining permission from the Competent Department, which today is NCSA's Personal Data Privacy Protection Department (PDPPD). Breaching the permit requirement carries a fine of up to QAR 5 million (Art. 24).

In practice the hospital must: map the processing in its ROPA; identify a permitted reason plus an additional condition; carry out a DPIA; submit NCSA's Special Nature Processing Permission Request form with the DPIA to the PDPPD; and wait for approval before processing. If the request is refused, the project must be revised or stopped.

### Cited Findings
- **Art. 16, full text** (CDP translation, [UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf)):
  - "The Personal data, related to ethnic origin, children, health, physical or psychological condition, religious creeds, marital relations, and criminal offenses, shall be regarded as Personal data with special nature."
  - "The Minister may add other types of Personal Data of a special nature, where the misuse or disclosure of the same may cause serious damage to Individual."
  - "Personal Data of a special nature may only be processed after obtaining the permission from the Competent Department, as per the measures and controls determined by a decision issued by the Minister."
  - "The Minister may, upon a decision therefrom, imposing additional precautions with the intent of protecting Personal Data of a special nature."
- **Penalty.** Art. 24 fines up to QAR 5,000,000 for breaching "(16\ paragraph 3)", which is the permit requirement ([UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf)).
- **Translation note on categories.** Commentaries render the list slightly differently, for example "race" or "ethnic origin", and "marriage relationships" or "marital status" ([search results summarising Simmons & Simmons, Squire Patton Boggs](https://www.simmons-simmons.com/en/publications/ck0bhphy2o64h0b33fg2coqvd/14-data-protection-update-qatar-introduces-a-law-on-personal-data-protection)). DLA Piper lists "relationships" ([DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=law&c=QA)).
- **Who grants the permit.** The CDP translation says the "Competent Department", meaning the administrative unit administering the PDPPL, now inside NCSA. The NCSA-hosted 2026 health deck says: "Personal data of a special nature may only be processed after obtaining the permission from the PDPPD" ([NCSA/PwC deck, Jan 2026](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/10207/1.0~fc4efdb1-0710-4db9-a751-c48e068c9509?mimetype=application%2Fpdf&filename=Presentation+-+Data+Privacy+in+Medical+Research+-+IDPD+2026+%282%29.pdf)).
- **Official procedure (NCSA PDPPD Advisory Note, Oct 2025, s.7.8 "Special Nature Processing"):**
  - "Identify Special Nature Data: Identify all processing activities which involve processing personal data with a special nature."
  - "Obtain Permission: … obtain permission from the PDPPD." This includes:
    - "Conducting a Data Privacy Impact Assessment (DPIA)";
    - "Identifying Permitted Reasons and Conditions: Document both a permitted reason for processing and an additional condition for special nature processing in their records";
    - "Submitting a Request: Submit a request for permission to process special nature personal data to the PDPPD."
  - "Enhanced Security Measures: Implement stronger security controls, such as encryption, access controls, and anonymization".
  - "Monitor and Review" on an ongoing basis.
  - The note cross-refers to the "Special Nature Processing - Guideline for Regulated Entities", PDPPL-02050215E.
  - Source: [Advisory Note](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/9737/1.0~b83017e6-db74-4592-a981-caae6512cbf8?mimetype=application%2Fpdf&filename=Advisory+Note+on+Building+a+Comprehensive+Data+Privacy+Program_EN_Final.pdf).
- **Health-research workflow (NCSA-hosted deck, Jan 2026).** For medical and scientific research involving health data:
  1. "Plan study & identify personal data with special nature"
  2. "Map personal data (RoPA), identify the permitted reason, lawful basis & conduct DPIA"
  3. "Fill out the Special Nature Processing Request form"
  4. "Submit the form and DPIA for PDPPD Approval"
  5. "Set up governance & agreements"
  6. "Share Personal Data"
  - "If proposal is refused, the project must be revised or stopped."
  - Also: "Obtain 'Special Nature Processing' permission and any necessary, ethics approvals before granting access to health or children's data."
  - Inputs to consider when seeking permission: the PDMS Checklist, the Privacy by Design guidelines, the "Permitted Reasons Guidelines", the Principles guidelines, and the DPIA Template.
  - Source: [NCSA/PwC deck](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/10207/1.0~fc4efdb1-0710-4db9-a751-c48e068c9509?mimetype=application%2Fpdf&filename=Presentation+-+Data+Privacy+in+Medical+Research+-+IDPD+2026+%282%29.pdf).
- **Where to find the guideline and form.** NCSA's Guidance Hub lists "Special Nature Processing - Guideline for Regulated Entities" and a companion "Special Nature Processing Permission Request" form. The hub was formerly at assurance.ncsa.gov.qa/en/privacy/hub and now redirects to [ncsa.gov.qa/en/pages/guidance-hub-for-regulated-entities](https://ncsa.gov.qa/en/pages/guidance-hub-for-regulated-entities). Hub contents are from search snippets; the page renders by script and I could not fetch it.
- **Two-part test (PDMS guideline, PDPPL-02050203E).** A controller handling special-nature data needs "a lawful purpose for processing and a separate condition for processing such data". The guideline also says a DPIA is generally expected for special-nature processing. Both points come from search-result snippets of the [PDMS Guideline](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/8872/1.0~b69114e4-5392-4851-81a8-6d7a7b39ac09?mimetype=application%2Fpdf&filename=Personal+Data+Management+System+%28PDMS%29+-+Guideline+for+Regulated+Entities+%282%29.pdf).
- **Law-firm descriptions of the procedure:**
  - **DLA Piper:** processing requires regulator authorisation, a permitted reason and an "additional condition", for example "explicit consent, data made public by the data subject, or necessity in an employment context". A DPIA is required, and the regulator may make permission conditional on the controller showing adequate administrative, technical and financial safeguards ([DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=law&c=QA)).
  - **Chambers 2026:** the permit application needs details of the processing, purpose, data subjects, recipients, transfers and safeguards ([Chambers 2026](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice)).
  - **Clyde & Co:** employers processing health data (medical leave, vaccination status and similar) must submit a "Special Nature Personal Data Form" to the regulator ([Clyde & Co](https://www.clydeco.com/en/insights/2021/03/new-regulatory-guidelines-on-the-qatar-persona-1)).
- **Data localisation (unverified).** The NCSA-hosted PwC deck lists, among "Key privacy updates in Qatar for 2026": "Data localization: Growing requirement to store personal data with special nature within Qatar on local or an approved cloud infrastructure" ([NCSA/PwC deck](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/10207/1.0~fc4efdb1-0710-4db9-a751-c48e068c9509?mimetype=application%2Fpdf&filename=Presentation+-+Data+Privacy+in+Medical+Research+-+IDPD+2026+%282%29.pdf)). Chambers 2026 says the PDPPL has no general localisation requirement ([Chambers 2026, s.5.3](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice)).

### Inferences
- **Every flow needs a permit.** Each hospital flow of identifiable or pseudonymised health data needs PDPPD permission before it starts: to the AI vendor, to insurers, and possibly to MoPH (see section 5). Art. 19 exempts controllers from Arts. 4, 5(1)–(3) and 6 only. It does **not** exempt them from Art. 16, so public-interest or research processing still needs the permit.
- **Permits likely attach to processing activities.** The Advisory Note says to identify "all processing activities" involving special-nature data and to obtain permission for "the identified … activities". So permits appear to be activity-specific, not institution-wide. This is an inference from the wording.
- **Localisation.** The 2026 localisation remark is a PwC observation, not a PDPPL article. It probably reflects cloud or sector policies. A governance lead should not cite it as a PDPPL requirement without a primary source.

### Gaps
- I found no published ministerial decision setting "the measures and controls" for special-nature permits, and none adding categories under Art. 16.
- I could not obtain the full text of the Special Nature Processing Guideline (PDPPL-02050215E) or the Permission Request form. Unconfirmed points: the exact list of "additional conditions", the processing time, the validity period, the fee (if any), and the submission channel (portal or email).
- I found nothing on whether MoPH-licensed healthcare providers have a sector-specific or blanket permit arrangement.

---

## 5. Exemptions and processing without consent (Arts. 4, 18–21)

### Takeaway
Consent is the default (Art. 4), but processing "necessary to achieve a Lawful Purpose" is an alternative basis.

Art. 19 exempts controllers from consent (Art. 4), from withdrawal, objection and erasure (Art. 5 items 1–3) and from access (Art. 6) in five cases:
- a public-interest task "as per the law";
- a legal obligation or court order;
- the vital interests of the individual;
- scientific research "underway for public interest";
- criminal investigation on official request.

Art. 18 lets a government "Competent Authority" set aside Arts. 4, 9, 15 and 17 for national security, international relations, state economic interests or crime.

There is **no express "public health" exemption**. None of these exemptions lifts the Art. 16 permit, security (Art. 13), data quality (Art. 10) or breach notification (Art. 14).

### Cited Findings
Article text from the [UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf) unless another source is given.

- **Art. 18, government purposes.** "The Competent Authority may decide to process some Personal Data, without abiding by the provisions of Articles (4), (9), (15) and (17) hereof, for achieving any of the following purposes":
  1. "Protecting National and public security."
  2. "Protecting international relations of the State."
  3. "Protecting the economic or financial interests of the State."
  4. "Preventing any criminal offense, or gathering information thereon or investigating therein."
  - The Competent Authority must keep a "special record". Conditions for entry on it are to be set by ministerial decision.
- **Art. 19, controller exemptions.** "The Controller shall be exempted from the provisions of Articles (4), (5\ Items 1, 2, and 3) and (6) hereof, in any of the following cases":
  1. "Executing a task related to the public interest as per the law."
  2. "Implementing a legal obligation or an order rendered by a competent court."
  3. "Protecting vital interests of Individual."
  4. "Achieving purposes of scientific research which is underway for public interest."
  5. "Gathering necessary information for investigation into a criminal offense, upon an official request of investigative bodies."
- **Arts. 20–21.** These cover refusals of access requests (see section 2).
- **Research in the guidance.** "guidelines clarify that public interest includes research 'of a wide benefit to society and economy'". Vital interests are illustrated as "an emergency medical incident when the individual is incapable of giving consent" ([NCSA/PwC deck, Jan 2026](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/10207/1.0~fc4efdb1-0710-4db9-a751-c48e068c9509?mimetype=application%2Fpdf&filename=Presentation+-+Data+Privacy+in+Medical+Research+-+IDPD+2026+%282%29.pdf)).
- **Secondary use (same deck).** For secondary processing, such as reusing treatment data for research "or to train a predictive risk model", the deck advises:
  - "Check compatibility with the original purpose and lawful basis (or seek consent …)";
  - "Obtain required ethics / governance approvals";
  - minimise and pseudonymise;
  - "Document the secondary purpose, legal basis, safeguards, and approvals in your … RoPA".
- **Data-sharing agreements (same deck).** Written data-sharing agreements are "not expressly required by the privacy law" but are best practice. The deck also advises: "Clearly identify who is controller and who is processor and record the lawful basis for each research collaboration".
- **Law-firm summaries.** Chambers 2026 describes Art. 18 as governmental exemptions and Art. 19 as including a limited public-interest research exemption ([Chambers 2026](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice)). DLA Piper lists the exemptions as public interest, legal obligation, vital interests, scientific research and crime investigation ([DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=law&c=QA)).
- **Employee data.** The 2020 guidelines say consent "is not advisable as a legal basis for processing for employees" ([Clyde & Co](https://www.clydeco.com/en/insights/2021/03/new-regulatory-guidelines-on-the-qatar-persona-1)).

### Inferences
- **MoPH reporting** (notifiable diseases, registries, licensing returns) would rest on Art. 19(2) "legal obligation" or Art. 19(1) "public interest as per the law". That requires a specific Qatari legal mandate. Consent, notice-based access and erasure duties are then lifted. The Art. 16 permit, Art. 13 security and Art. 14 breach duties still apply on the text, unless MoPH itself acts as an Art. 18 "Competent Authority", which covers security and crime purposes only, not public health.
- **Insurer disclosures** are not covered by an Art. 19 exemption unless a law mandates them. They would rely on patient consent or on Art. 4 "necessary to achieve a Lawful Purpose", plus the Art. 16 permit.
- **AI vendor processing** for direct care could rely on Art. 4 Lawful Purpose. Reuse for model development would need consent or the Art. 19(4) public-interest research exemption, plus ethics approval, the Art. 16 permit and a DPIA.
- **Notice is still owed.** Art. 19 does not exempt from Art. 9 (prior notice). Only the Art. 18 government route does. So even exempt processing still needs a privacy notice.

### Gaps
- I did not obtain the text of NCSA's "Permitted Reasons" (lawful purposes) guideline, so the official list of Lawful Purposes and "additional conditions" is unverified.
- I did not research sector-specific Qatari health laws (for example on communicable disease reporting, medical records or MoPH health information policies) that would supply the "legal obligation" for MoPH sharing. These are out of scope here but needed for the mapping.

---

## 6. Breach notification (Arts. 11(5), 13, 14)

### Takeaway
The law requires the controller to inform both the individual and the Competent Department of a breach that "may cause serious damage", and requires processors to notify the controller "forthwith". It sets no deadline. NCSA guidance sets **72 hours from becoming aware** for both the regulator and affected individuals. Notification to the regulator is made through the NCSA Breach Notification Form.

### Cited Findings
- **Art. 14.** "The Controller shall inform the Individual and Competent Department of the occurrence of any breach of the precautions provided for in the preceding Article, and if such breach may cause serious damage to Personal Data or individual privacy" ([UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf)). The NCSA translation reads: "The Controller shall inform both the relevant individual and Competent Department upon occurrence of a breach of such precautions, if this breach may cause serious damage either to Personal Data or relevant individual privacy." ([Breach Guideline](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/2991/1.0~5b70754f-6861-4223-8368-b0c74bd1a261?mimetype=application%2Fpdf&filename=BGJ.pdf)).
- **Art. 13.** The processor "shall forthwith notify the Controller" of any breach or risk ([UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf)).
- **NCSA Personal Data Breach Notifications Guideline, PDPPL-02050217E, v2.0** (first published Nov 2020, updated Sept 2022; [PDF](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/2991/1.0~5b70754f-6861-4223-8368-b0c74bd1a261?mimetype=application%2Fpdf&filename=BGJ.pdf); a later copy is on the hub at [doc 8870](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/8870/1.0~740b1248-e3a9-40e1-b66e-589091cc182a?mimetype=application%2Fpdf&amp=&filename=Personal+Data+Breach+Notifications+-+Guideline+for+Regulated+Entities+%284%29.pdf)):
  - **Definition:** "a breach of security leading to the unlawful or accidental alteration, destruction, loss, unauthorised disclosure of, or access to, personal data".
  - **Deadline:** "Controllers must notify the National cyber governance and assurance affairs and individuals of a personal data breach within 72 hours of becoming aware of the breach where the breach can cause serious damage to individuals." Elsewhere: report to the regulator "without delay and within 72 hours of becoming aware of it, if the personal data breach could cause damage", and notify individuals "without delay and within 72 hours … if the personal data breach could cause serious damage".
  - **Incomplete information:** if the facts are not complete, notify within 72 hours with the information available. Include "the reasons why they are not able to provide all the required information" and "how and when they will be able to provide further information".
  - **Accountability:** controllers "should document the rationale of their decision on whether or not to report", especially when deciding not to report. Wrongly not reporting is non-compliance with Art. 14, with a penalty under Art. 23.
  - **Channel:** "via the breach notification page on the [regulator's] website using the Breach Notification Form". The related form is PDPPL-02040402E.
  - **Content of the regulator notice:** the nature of the breach, "categories of individuals concerned, the types of personal data involved and an estimated number of individuals and personal data records concerned"; a privacy contact; likely consequences; and actions taken or proposed, including mitigation.
  - **Content of the individual notice:** sent "directly to them", in "clear and plain language", with the contact point, likely consequences and remedial actions. Controllers may consult the regulator first.
  - **Breach response framework:** awareness, internal escalation, confidentiality, triage, response team, scoping, serious-damage assessment, notification, closure, and documenting lessons learnt. Regular breach exercises and training are expected.
  - **What the regulator may examine after notification:** the circumstances, the data affected, precautions in place ("a data privacy and protection policy; an information security policy; … encryption, firewalls … periodic mandatory staff training"), third-party contracts and processor due diligence, and the timeliness of notifications.
  - **Penalties cited in the guideline:** failure to notify, up to QAR 1,000,000 per violation (Art. 23); inadequate precautions, up to QAR 5,000,000 (Art. 24); a processor's failure to inform the controller, up to QAR 5,000,000 (Art. 24).
  - **Legal mandate statement:** "Based on the Amiri Decree No. (1) for the year 2021, the National Cyber Governance and Assurance Affairs is empowered by the National Cyber Security Agency (NCSA) as the competent department for administrating and enforcing Law no (13) for the year 2016."
- **72 hours in secondary sources.** The 72-hour standard dates from the November 2020 guidelines ([Clyde & Co](https://www.clydeco.com/en/insights/2021/03/new-regulatory-guidelines-on-the-qatar-persona-1)). DLA Piper confirms it ([DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=law&c=QA)). Chambers 2026 omits the deadline ([Chambers 2026](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice)).

### Inferences
- **Hospital and vendor timing.** The 72-hour clock runs from the hospital's awareness. Contracts with the AI vendor, and any other processor, should therefore require notice "forthwith", for example within 24 hours, so the hospital can meet 72 hours.
- **Health breaches are usually reportable.** Special-nature data is the first listed severity factor, so most health-data breaches will meet the "serious damage" threshold.
- **Guidance vs. statute.** The 72-hour figure comes from guidance, not the statute. A breach report should cite "Art. 14 PDPPL; NCSA Breach Notification Guideline PDPPL-02050217E (72 hours)".

### Gaps
- The guideline copy read is v2.0 (Sept 2022), branded NCGAA. I could not confirm whether a later version under the PDPPD brand changed anything, or the current URL of the online breach form.

---

## 7. Cross-border transfer (Art. 15)

### Takeaway
Art. 15 is framed unusually. It bars the controller from restricting cross-border data flows, unless the processing breaches the PDPPL or "may cause serious damage". In effect, transfers abroad are allowed in principle but are subject to the full law. NCSA guidance expects transfers to be recorded, risk-assessed (DPIA) and contractually protected so that the importer processes the data in line with the PDPPL. There are no adequacy decisions or prescribed standard clauses.

### Cited Findings
- **Art. 15.** "Taking into account the liabilities provided for hereto, the Controller shall be forbidden from taking any decision or measure that may limit the Cross-Border Data Flow, unless the processing of such data is in breach of this Law, or where such processing may cause serious damage to the Personal [Data or the Individual's privacy]" ([UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf); the tail is a missing fragment). DLA Piper paraphrases it as "gross damage to the data subject" ([DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=law&c=QA)).
- **Penalty.** Breach of Art. 15: up to QAR 1,000,000 (Art. 23) ([UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf)).
- **Government exemption.** Art. 18 lets a Competent Authority disregard Art. 15 for security, crime and similar purposes ([UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf)).
- **NCSA Advisory Note (Oct 2025).** To manage cross-border risk, the organisation should:
  - "Identify and record all cross-border data transfers of personal data";
  - "Perform a risk assessment to identify and manage any risks that may arise from such data transfers";
  - "Ensure the data importing entity established outside Qatar processes personal data in accordance with PDPPL requirements … via appropriate contractual measures".
  - Privacy notices must give "Details of any cross-border data disclosures".
  - Source: [Advisory Note](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/9737/1.0~b83017e6-db74-4592-a981-caae6512cbf8?mimetype=application%2Fpdf&filename=Advisory+Note+on+Building+a+Comprehensive+Data+Privacy+Program_EN_Final.pdf).
- **Breach Guideline.** "undertaking a cross-border personal data transfer i.e. transferring personal data outside of the State of Qatar" is listed as a factor that increases severity and points to a DPIA ([Breach Guideline](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/2991/1.0~5b70754f-6861-4223-8368-b0c74bd1a261?mimetype=application%2Fpdf&filename=BGJ.pdf)).
- **NCSA-hosted health deck (Jan 2026).** Any transfer outside Qatar must comply and not "cause serious damage to personal data or privacy, backed by a documented Data Protection Impact Assessment and PDPPD-compliant contractual safeguards". Example: "SCCs, data sharing agreement, etc." ([NCSA/PwC deck](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/10207/1.0~fc4efdb1-0710-4db9-a751-c48e068c9509?mimetype=application%2Fpdf&filename=Presentation+-+Data+Privacy+in+Medical+Research+-+IDPD+2026+%282%29.pdf)).
- **Chambers 2026.** Transfers are "permitted in principle". No transfer mechanisms such as adequacy decisions or SCCs are prescribed. There is no general localisation requirement, and "There have been no recent developments in the regulation of the international transfer of personal data" (ss.5.1, 5.3, 5.5) ([Chambers 2026](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice)).
- **2020 guidelines.** DPIAs were expected for "prospective data exports" ([Clyde & Co](https://www.clydeco.com/en/insights/2021/03/new-regulatory-guidelines-on-the-qatar-persona-1)).

### Inferences
- **Overseas AI vendors.** If the AI vendor hosts or processes data outside Qatar, the hospital needs:
  - a DPIA covering the transfer;
  - a contract binding the vendor to PDPPL-equivalent protection;
  - an entry in the ROPA and privacy notice;
  - the Art. 16 permit application disclosing the transfer (Chambers says applications cover transfers).
- **Other localisation rules.** Separate cloud or health-sector rules may require in-country hosting of health data. This was not verified here (see section 4).

### Gaps
- I did not obtain the cross-border section, if any, of the NCSA Principles, DPIA or Special Nature guidelines.
- I did not verify any MoPH or national cloud-policy localisation rule for health data.

---

## 8. Automated processing and profiling, direct marketing, children

### Takeaway
- **Automated decisions.** The PDPPL has no article on automated decision-making or profiling. NCSA guidance requires human review on objection, disclosure in privacy notices, and treats automated decision-making as a high-risk trigger for a DPIA.
- **Direct marketing.** Electronic direct marketing needs prior consent (Art. 22).
- **Children.** Children's data is special-nature data (Art. 16). Websites aimed at children must meet the Art. 17 duties, including explicit guardian consent, with fines of up to QAR 5 million (Art. 24).

### Cited Findings
- **Automated decisions in the law.** There is no PDPPL provision. Chambers 2026 says automated decision-making is "Not addressed" in the law, and that AI processing must meet PDPPL standards, with Art. 16 approval for sensitive data ([Chambers 2026, s.1.5](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice)).
- **Automated decisions in guidance:**
  - The Individuals' Rights Guidelines (2026 coverage) say, under the Art. 5(2) objection right, that controllers must "provide human review for automated decisions" ([The Peninsula, 18 Apr 2026](https://www.thepeninsulaqatar.com/article/18/04/2026/explainer-ncsa-issues-guidelines-on-individuals-personal-data-privacy-protection-law-in-qatar)).
  - Privacy notices must include "Details of any automated decision-making including profiling" ([Advisory Note](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/9737/1.0~b83017e6-db74-4592-a981-caae6512cbf8?mimetype=application%2Fpdf&filename=Advisory+Note+on+Building+a+Comprehensive+Data+Privacy+Program_EN_Final.pdf)).
  - Automated decision-making that limits access to a "product, service, opportunity or benefit" ("decisions made by a computer without human involvement") is a high-severity indicator ([Breach Guideline](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/2991/1.0~5b70754f-6861-4223-8368-b0c74bd1a261?mimetype=application%2Fpdf&filename=BGJ.pdf)).
- **AI guidance.** NCSA has issued "Guidelines for Secure Adoption and Usage of Artificial Intelligence", which address privacy, bias and security risks "particularly in sectors where AI processes personal data (such as finance, healthcare and law enforcement)" ([Chambers 2026](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice); search-result summary). NCSA's Jan 2026 event also included a session titled "Implementing Responsible and Compliant AI Systems" ([NCSA PDF](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/10209/1.0~926129d6-931a-48dd-b185-7e15bb07e2fa?mimetype=application%2Fpdf&filename=Presentation+-+Implementing+Responsible+and+Compliant+AI+Systems+-+IDPD+2026+%2810%29.pdf); not read).
- **Art. 22, direct marketing.** "The transmission of any Electronic Communication to an Individual, for the purpose of Direct Marketing, shall be forbidden, except after obtaining the prior consent thereof." The message must identify the sender, state that it is direct marketing, and include "a valid address … through which an Individual can send a request … to stop such communications or revoke the consent". Penalty: up to QAR 1m (Art. 23) ([UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf)).
- **Marketing consent in guidance.** Consent "must be explicit, unambiguous and a clear, affirmative statement"; pre-ticked boxes and implied consent may not be valid ([Clyde & Co](https://www.clydeco.com/en/insights/2021/03/new-regulatory-guidelines-on-the-qatar-persona-1)). Chambers says Art. 22 does not recognise implied consent ([Chambers 2026, s.4.2](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice)).
- **Art. 17, websites addressing children.** "an owner or operator of any website addressing children" must:
  1. post a notice on what child data is collected, how it is used and the disclosure policies;
  2. obtain "either electronically or through any other appropriate means, an explicit consent from the guardian";
  3. give the guardian, on request and after identity verification, a description of the data, the purpose and a copy;
  4. delete or stop processing at the guardian's request;
  5. [not make a child's participation in an activity conditional on providing] "Data in excess of the necessary for the participation in such activity". The bracketed wording is a missing fragment and is reconstructed.
  - Penalty: up to QAR 5m (Art. 24). A Competent Authority may disregard Art. 17 under Art. 18.
  - Source: [UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf).
- **Children in the 2026 deck.** "Children's data is classified as 'personal data with special nature' and may only be processed with explicit consent from the child's guardian and, where applicable, subject to additional precautions" ([NCSA/PwC deck](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/10207/1.0~fc4efdb1-0710-4db9-a751-c48e068c9509?mimetype=application%2Fpdf&filename=Presentation+-+Data+Privacy+in+Medical+Research+-+IDPD+2026+%282%29.pdf)).

### Inferences
- **AI diagnostic tool.** It should be designed with clinician-in-the-loop review, so that decisions are not fully automated. It should be disclosed in the privacy notice and DPIA'd as "new innovative technology" and "automated decision-making".
- **Paediatric records** carry two special-nature categories, children and health, which reinforces the need for the permit.
- **Patient portals and apps.** Hospital marketing by SMS or email, for example health-check promotions, needs prior opt-in consent. A paediatric patient portal could fall within Art. 17.

### Gaps
- The PDPPL does not define "child" or set an age; I found no guidance defining it.
- I did not read the full text of the NCSA AI guidelines.

---

## 9. Penalties and enforcement (Arts. 23–26, 29)

### Takeaway
Fines go up to QAR 1 million (Art. 23) or QAR 5 million (Art. 24) per violation, plus up to QAR 1 million for a legal person (Art. 25). The heaviest tier covers security failures, processing special-nature data without a permit, and children's websites.

The regulator's direct tool is a binding, reasoned rectification order (Art. 26). The order can be appealed to the Minister within 60 days. NCSA has issued such orders since December 2024.

### Cited Findings
Article text from the [UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf).

- **Art. 23.** "Without prejudice to any more severe penalty stipulated in any other law, a penalty that shall not exceed (1,000,000) one million QR shall be applicable to anyone violating any of the provisions of the Articles (4, 8, 9, 10, 11, 12, 14, 15, and 22)."
- **Art. 24.** A penalty "that shall not exceed (5,000,000) five million QR" for violating "Articles (13), (16\ paragraph 3), and (17)".
- **Art. 25.** A penalty "that shall not exceed (1,000,000) One million QR shall be applicable to violating legal person, in the event of committing any of those crimes stipulated herein on the name or for the interest thereof, without prejudice to criminal liability taken by affiliated natural person."
- **Art. 26, complaints and rectification orders.**
  - The Competent Department may, "after investigating received complaints and proving the seriousness thereof, issue a reasoned decision binding the Controller or Processor … to rectify such breach within a period it specifies".
  - The controller or processor may raise a grievance with the Minister "within sixty days from the notification date".
  - The Minister decides within sixty days; silence is "an implicit rejection"; the Minister's decision "shall be final".
- **Art. 27.** Gives the Competent Department general implementation powers: coordination with professional associations, child online safety, and research.
- **Art. 29.** Ministry employees given law-enforcement (judicial officer) status by decision of the Public Prosecutor, "in agreement with the Minister, may detect and prove crimes committed in violation" of the law.
- **"Per violation" wording.** The NCSA Breach Guideline describes the fines "per violation" ([Breach Guideline](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/2991/1.0~5b70754f-6861-4223-8368-b0c74bd1a261?mimetype=application%2Fpdf&filename=BGJ.pdf)).
- **Missing DPIA.** Clyde & Co cites "QAR 1,000,000 … for failing to carry out a DPIA", which corresponds to Art. 11(1) via Art. 23 ([Clyde & Co](https://www.clydeco.com/en/insights/2021/03/new-regulatory-guidelines-on-the-qatar-persona-1)).
- **Enforcement decisions** by NCSA's National Data Privacy Office (NDPO) ([Baker McKenzie Connect On Tech, 15 Apr 2025](https://connectontech.bakermckenzie.com/data-protection-enforcement-update-qatar/)):
  - **December 2024, ICT company.** Followed a 2023 complaint about use of personal data without consent. Breaches found: processing without consent or a lawful purpose, inadequate safeguards, data accuracy, and failure to oversee third-party processors. The company was ordered to enhance and monitor administrative, technical and financial measures. It avoided public censure because of its cooperation.
  - **March 2025, e-commerce company.** Followed a breach investigation. Breaches found in consent, safeguards, accuracy and supervision. The company was ordered to strengthen compliance.
  - **April 2025, contracting company.** Breached "numerous provisions". It was given a binding order with "a 60-day period from the date of the decision to comply".
- **Conflicting view.** Chambers 2026 says there are "no widely reported, publicly available enforcement actions specifically under the PDPPL" in the past 24 months ([Chambers 2026, s.1.9](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice)). This conflicts with Baker McKenzie.
- **Who imposes fines.** Secondary sources say the regulator "can … impose fines of up to 5 million" ([DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=law&c=QA)), and the NCSA-hosted deck says "The competent authority can issue binding decisions and impose fines, which can reach up to 5 million QAR" ([NCSA/PwC deck](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/10207/1.0~fc4efdb1-0710-4db9-a751-c48e068c9509?mimetype=application%2Fpdf&filename=Presentation+-+Data+Privacy+in+Medical+Research+-+IDPD+2026+%282%29.pdf)).

### Inferences
- **Fines may be criminal.** The text describes the Arts. 23–25 offences as "crimes" (Art. 25), and enforcement uses judicial officers named by the Public Prosecutor (Art. 29). The fines therefore look criminal, imposed through prosecution and the courts. The regulator's own direct remedy is the Art. 26 rectification order. Secondary sources describe the fines loosely as regulator-imposed. Report authors should phrase this as "penalties of up to QAR X under Art. 23/24".
- **Highest-exposure articles for a hospital:** Art. 13 (security), Art. 16(3) (permit) and Art. 17 (children's sites), at QAR 5m each.

### Gaps
- I did not verify whether any fine (as opposed to a rectification order) has actually been imposed under the PDPPL.
- The total penalties for multiple violations (cumulative per violation or capped) are not addressed in the law text.

---

## 10. Competent authority as of 2026

### Takeaway
The law names the Ministry of Transport and Communications (MoTC) and its "competent administrative unit". In 2016–2020 that unit was the MoTC Compliance and Data Protection (CDP) Department. Under Amiri Decree (Decision) No. 1 of 2021, the National Cyber Security Agency (NCSA) took over: first through its National Cyber Governance and Assurance Affairs (NCGAA), then through the National Data Privacy Office (NDPO, cited 2024–2025).

As of late 2025–2026, the competent department is NCSA's **Personal Data Privacy Protection Department (PDPPD)**, described as "formerly the National Data Privacy Office". Its guidance is on ncsa.gov.qa. The old assurance.ncsa.gov.qa privacy pages now redirect there, and compliance.qcert.org was the CDP's earlier site.

### Cited Findings
- **Original allocation.** Art. 1 defines the Ministry as "Ministry of Transport and Communications" and the Competent Department as "the competent administrative unit at the Ministry". The translation PDF is branded "Compliance and Data Protection (CDP) department compliance.qcert.org" ([UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf)).
- **2020 guidelines.** The MoTC CDP issued 14 regulatory guidelines in November 2020 ([Clyde & Co, 15 Mar 2021](https://www.clydeco.com/en/insights/2021/03/new-regulatory-guidelines-on-the-qatar-persona-1)).
- **2022 guideline mandate.** "Based on the Amiri Decree No. (1) for the year 2021, the National Cyber Governance and Assurance Affairs is empowered by the National Cyber Security Agency (NCSA) as the competent department for administrating and enforcing Law no (13) for the year 2016" ([Breach Guideline v2.0, Sept 2022](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/2991/1.0~5b70754f-6861-4223-8368-b0c74bd1a261?mimetype=application%2Fpdf&filename=BGJ.pdf)). The same text says the guidelines were "prepared by the Compliance and Data Protection (National cyber governance and assurance affairs) Department".
- **2024–2025 enforcement.** Decisions were issued by the "National Data Privacy Office ('NDPO'), part of the National Cyber Security Agency" ([Baker McKenzie, 15 Apr 2025](https://connectontech.bakermckenzie.com/data-protection-enforcement-update-qatar/)).
- **October 2025 mandate.** The Advisory Note is issued by "National Cyber Security Agency (NCSA) Personal Data Privacy Protection Department (PDPPD)". It states: "Based on the Amiri Decree No. (1) for the year 2021, the Personal Data Privacy Protection Department is empowered by the National Cyber Security Agency (NCSA) as the competent department for administrating and enforcing Law no (13) for the year 2016" ([Advisory Note, Oct 2025](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/9737/1.0~b83017e6-db74-4592-a981-caae6512cbf8?mimetype=application%2Fpdf&filename=Advisory+Note+on+Building+a+Comprehensive+Data+Privacy+Program_EN_Final.pdf)).
- **January 2026 deck.** "The National Cyber Security Agency (NCSA), through the Personal Data Privacy Protection Department (PDPPD) (formerly the National Data Privacy Office) is the official regulatory authority responsible for administering and enforcing the … PDPPL", "Established by Amiri Decree No. (1) of 2021" ([NCSA/PwC deck](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/10207/1.0~fc4efdb1-0710-4db9-a751-c48e068c9509?mimetype=application%2Fpdf&filename=Presentation+-+Data+Privacy+in+Medical+Research+-+IDPD+2026+%282%29.pdf)).
- **June 2026.** NCSA described the PDPPD's remit: enforcing the law and overseeing compliance across sectors; implementing laws, regulations and decisions; proposing requirements, standards and frameworks; "Issuing regulatory instruments, including policies, guidelines, and supporting tools"; research "with a focus on sensitive data categories"; awareness; and international representation. Complaints go to the "Personal Data Privacy Protection Administration" ([The Peninsula, 10 Jun 2026](https://www.thepeninsulaqatar.com/article/10/06/2026/ncsa-highlights-key-role-of-pdppd-in-safeguarding-privacy-rights)).
- **Web addresses.** assurance.ncsa.gov.qa/en/privacy/law now returns a 301 redirect to ncsa.gov.qa/en/pages/personal-data-privacy-personal-data-privacy-protection-law, and /privacy/hub redirects to ncsa.gov.qa/en/pages/guidance-hub-for-regulated-entities. I observed these redirects during this research on 22 Nov 2026; the target pages render by script.
- **Conflicting secondary sources:**
  - Chambers 2026 calls the "CDPD at the MCIT … the key regulator", with NCSA "the competent department for administration and enforcement" (s.1.7). In s.1.8 it says the competent department was "not yet designated" ([Chambers 2026](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice)).
  - DLA Piper (last modified 17 Jan 2024) names NCSA's NCGAA ([DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=law&c=QA)).
  - Both are outdated or inconsistent compared with NCSA's own 2025–2026 documents.

### Inferences
- **For 2026 citations:** "the Competent Department under Art. 1 PDPPL, currently NCSA's Personal Data Privacy Protection Department (PDPPD), pursuant to Amiri Decree No. 1 of 2021". Earlier names (MoTC CDP, NCGAA, NDPO) should be labelled historical.
- **Who holds the "Minister" powers today is unclear.** These are the Art. 26 grievances and the Arts. 7, 8, 16 and 18 decisions. Logically they sit with NCSA's head, but I found no source saying so.

### Gaps
- I did not read the text of Amiri Decree No. 1 of 2021 on Al Meezan, so I have not confirmed the exact transfer wording, or whether "Minister" powers moved to the NCSA President.
- I did not find the date the NDPO was renamed PDPPD. It happened by October 2025 at the latest.

---

## 11. Official guidelines: what they require in practice

### Takeaway
The regulator's guidelines are non-binding interpretations ([Chambers 2026](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice)), but they are used in enforcement. They form a numbered suite first issued in November 2020 and updated (v2.0) in September 2022. Further documents followed: an Advisory Note on building a privacy programme (October 2025) and Individuals' Rights Guidelines publicised in April 2026.

Together they require: a PDMS; a ROPA; DPIAs; privacy by design and default; privacy notices; processor contracts; 72-hour breach notification; 30-day handling of rights requests; and special-nature permits.

### Cited Findings
- **Guideline suite (reference numbers from the Oct 2025 Advisory Note and the Sept 2022 Breach Guideline):**
  - PDPPL-02050201E Principles of Data Privacy
  - PDPPL-02050203E Personal Data Management System (PDMS) guideline
  - PDPPL-02040203E PDMS Checklist
  - PDPPL-02050205E Individuals' Rights
  - PDPPL-02050206E Data Privacy Impact Assessment (DPIA)
  - PDPPL-02050208E Data Privacy by Design and by Default
  - PDPPL-02050209E Controller and Processor
  - PDPPL-02050212E Record of Processing Activities
  - PDPPL-02050213E Privacy Notice
  - PDPPL-02050215E Special Nature Processing
  - PDPPL-02050217E Personal Data Breach Notifications
  - PDPPL-02040402E Personal Data Breach Notifications Form
  - Tools: Organization Level Privacy Compliance Assessment Tool; Privacy by Design Assessment Tool; DPIA Template; Vendor Privacy Management Tool; National Incident Management Framework.
  - Sources: [Advisory Note](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/9737/1.0~b83017e6-db74-4592-a981-caae6512cbf8?mimetype=application%2Fpdf&filename=Advisory+Note+on+Building+a+Comprehensive+Data+Privacy+Program_EN_Final.pdf); [Breach Guideline](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/2991/1.0~5b70754f-6861-4223-8368-b0c74bd1a261?mimetype=application%2Fpdf&filename=BGJ.pdf).
  - Also referenced: a "Permitted Reasons Guidelines" document and an NCSA ROPA template ([NCSA/PwC deck](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/10207/1.0~fc4efdb1-0710-4db9-a751-c48e068c9509?mimetype=application%2Fpdf&filename=Presentation+-+Data+Privacy+in+Medical+Research+-+IDPD+2026+%282%29.pdf)), and the "Special Nature Processing Permission Request" form on the hub ([Guidance Hub](https://ncsa.gov.qa/en/pages/guidance-hub-for-regulated-entities); from search snippet).
- **Advisory Note on Building a Comprehensive Data Privacy Program**, PDPPL-202501AN(E), v1.0, October 2025, NCSA PDPPD. It sets out a phased programme (Phase III "Implement" and Phase IV "Sustain" are named in the text; the earlier phases were not extracted). Phase III covers:
  - policies and procedures;
  - personal data lifecycle management;
  - privacy notices;
  - third-party and cross-border risk;
  - individual rights;
  - special-nature processing;
  - breach management;
  - privacy by design.
  - It recommends a Data Privacy Office or Officer, top-management approval of policies, staff training and clear disposal procedures "in line with the organization's data retention policies".
  - Source: [Advisory Note](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/9737/1.0~b83017e6-db74-4592-a981-caae6512cbf8?mimetype=application%2Fpdf&filename=Advisory+Note+on+Building+a+Comprehensive+Data+Privacy+Program_EN_Final.pdf).
- **Individuals' Rights Guidelines** (NCSA, publicised 18 April 2026): an article-by-article explanation of the rights, a 30-day erasure response, and human review of automated decisions ([The Peninsula](https://www.thepeninsulaqatar.com/article/18/04/2026/explainer-ncsa-issues-guidelines-on-individuals-personal-data-privacy-protection-law-in-qatar)).
- **What the 2020 guidelines required:** a PDMS, ROPA, DPIAs, privacy by design and default, prescriptive notices, processor due diligence and contracts, 30-day rights responses, 72-hour breach notification, special-nature authorisation and explicit marketing consent ([Clyde & Co](https://www.clydeco.com/en/insights/2021/03/new-regulatory-guidelines-on-the-qatar-persona-1)).
- **Medical research deck.** The NCSA-hosted health deck (Jan 2026) recommends a "structured data protection program" for special-nature health data, made up of: strategy and operating model, ROPA, risk assessments, Data Processing Agreements, policies and notices, and training ([NCSA/PwC deck](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/10207/1.0~fc4efdb1-0710-4db9-a751-c48e068c9509?mimetype=application%2Fpdf&filename=Presentation+-+Data+Privacy+in+Medical+Research+-+IDPD+2026+%282%29.pdf)).

### Inferences
- **A mapping checklist.** These elements give the governance lead a ready checklist: ROPA, DPIA, privacy by design, notice, rights procedure, processor contract, breach plan, special-nature permit, DPO and training. Each can be mapped to its PDPPL article: Arts. 8, 9, 10, 11, 12, 13, 14 and 16 respectively.

### Gaps
- I did not obtain the full original 14-title list from November 2020.
- I did not verify whether the Sept 2022 v2.0 guidelines were reissued under the PDPPD brand in 2025–2026.
- The "Personal Data Privacy" portal and the online permit and breach submission systems could not be inspected, because the pages render by script.

---

## 12. Amendments, executive regulations and decisions since 2016

### Takeaway
I found no amendment to Law No. 13 of 2016 and no published executive regulations or ministerial decisions under Arts. 7, 8, 16, 18 or 31. Changes since 2016 are institutional and soft-law:
- 2020: guidelines issued;
- 2021: NCSA created by Amiri Decree No. 1 of 2021 and given the PDPPL mandate;
- 2022: guidelines v2.0;
- 2024–2025: first enforcement orders;
- 2025: PDPPD Advisory Note;
- 2026: Individuals' Rights Guidelines and AI and health awareness material.

### Cited Findings
- **No amendments or regulations reported.** Chambers 2026 reports no amendments or executive regulations, and says Qatar "may follow suit" with updates without anything being enacted ([Chambers 2026](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice)). DLA Piper mentions no amendments ([DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=law&c=QA)).
- **Implementing decisions.** Art. 31 says "The Minister shall issue the necessary decisions for the implementation". Arts. 7, 8(4), 16 and 18 each anticipate ministerial decisions ([UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf)). Guidelines say they should be read with "any related ministerial decisions" without naming any ([Breach Guideline](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/2991/1.0~5b70754f-6861-4223-8368-b0c74bd1a261?mimetype=application%2Fpdf&filename=BGJ.pdf)).
- **Transition period.** Art. 30 gave six months from entry into force to comply, extendable by the Council of Ministers ([UNIDIR PDF](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf)). A vLex/Mondaq headline indicates there were no further Council of Ministers extensions ([vLex](https://vlex.com/vid/qatar-s-data-privacy-731324181); headline only, not read).
- **"2026 updates" listed in the NCSA-hosted PwC deck.** These include: criminal sanctions for photographing or sharing images of people in public without consent (up to 1 year and/or QAR 100,000); a "growing requirement" for in-country storage of special-nature data; stricter marketing consent; "Mandatory DPIAs … with fines up to QAR 1 million"; and AI and Open Data Policy (v2.0.0) oversight ([NCSA/PwC deck](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/10207/1.0~fc4efdb1-0710-4db9-a751-c48e068c9509?mimetype=application%2Fpdf&filename=Presentation+-+Data+Privacy+in+Medical+Research+-+IDPD+2026+%282%29.pdf)). The deck gives no citations for these. The photography sanction presumably comes from a different law (for example Penal Code or cybercrime amendments), not the PDPPL.
- **Photography sanction source.** The criminal sanction for publishing images without consent comes from **Law No. 11 of 2025**, which amends the Cybercrime Law (Law No. 14 of 2014). It was published in Official Gazette No. 20 of 2025 on 4 August 2025, adds Art. 8 (bis), and allows up to 1 year in prison and/or a fine of up to QAR 100,000 for unauthorised online publication of images or videos of individuals. It is **not** a PDPPL amendment ([Mondaq, "Qatar introduces new penalties for privacy violations"](https://www.mondaq.com/privacy-protection/1670196/qatar-introduces-new-penalties-for-privacy-violations); details from a search-result summary, not read in full).
- **Cloud privacy assessment tool.** NCSA launched a cloud privacy assessment tool in spring 2026 to help organisations meet PDPPL requirements ([The Peninsula, 3 Apr 2026](https://thepeninsulaqatar.com/article/03/04/2026/qatar-launches-cloud-privacy-assessment-tool-to-strengthen-data-protection); headline and snippet only).
- **June 2026 campaign.** NCSA ran an awareness campaign on X about the PDPPD ([The Peninsula, 10 Jun 2026](https://www.thepeninsulaqatar.com/article/10/06/2026/ncsa-highlights-key-role-of-pdppd-in-safeguarding-privacy-rights)).
- **September 2026 campaign: seven principles.** NCSA's PDPPD, under the slogan "Data Privacy Starts with You", set out seven principles mapped to PDPPL articles:
  1. Transparency, honesty and dignity: Art. 3.
  2. Integrity and confidentiality: Arts. 3, 8(3), 13.
  3. Purpose limitation: Arts. 5(3), 10.
  4. Data minimisation, "necessary and relevant": Art. 10.
  5. Accuracy: Art. 10.
  6. Storage limitation, "longer than necessary to achieve lawful objectives": Art. 10.
  7. Accountability, internal management systems and reporting of breaches: Art. 11(5).
  - The campaign mentioned no new decisions or amendments.
  - Source: [The Peninsula, 6 Sep 2026](https://www.thepeninsulaqatar.com/article/06/09/2026/ncsa-highlights-core-personal-data-privacy-protection-principles).
- **No 2026 amendment found.** A November 2026 search found no amendment to Law No. 13 of 2016 and no NCSA decision changing it. Coverage through September 2026 still cites the 2016 law as the governing statute ([The Peninsula, 6 Sep 2026](https://www.thepeninsulaqatar.com/article/06/09/2026/ncsa-highlights-core-personal-data-privacy-protection-principles); [Chambers 2026](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice)).

### Inferences
- **The 2016 text remains current law** as of November 2026. Practical obligations such as the 72 hours, 30 days, DPIAs, contracts and the permit procedure come from NCSA guidance and practice, and should be cited as guidance, not statute.

### Gaps
- I could not search Al Meezan directly for 2024–2026 decisions. A check of Al Meezan and the Official Gazette for any NCSA or ministerial decision under the PDPPL is recommended before the report is finalised.
- I did not verify the PwC deck's "2026 updates" against primary sources.
