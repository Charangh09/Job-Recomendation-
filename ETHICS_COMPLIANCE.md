# ETHICS & COMPLIANCE STATEMENT

**SHL Assessment Recommendation System**  
**Version 1.0 | December 16, 2025**

---

## 1. DATA ETHICS

### 1.1 Data Source & Attribution
✅ **Commitment:**
- All assessment data sourced from public SHL product pages
- No proprietary or internal SHL information used
- Public descriptions and information only
- Proper attribution to SHL Product Catalog

✅ **Verification:**
```python
Data source: https://www.shl.com/en/products/
Access: Public, no authentication required
Permission: Educational/prototype use acceptable
Usage: Demonstration and testing only
```

### 1.2 Data Privacy
✅ **User Data Protection:**
- No user data stored or retained
- Job descriptions used temporarily during session
- No analytics tracking
- Recommendations never persisted
- No cookies or session tracking

✅ **Implementation:**
```python
# Recommendations discarded after display
results = recommender.recommend(...)
# User can see results
# No storage occurs
# User can refresh/start new search
```

### 1.3 Data Transparency
✅ **What Users See:**
- All data sources identified
- Assessment definitions shown in full
- Match calculations explained
- Similarity scores disclosed
- Model information provided

---

## 2. ALGORITHMIC FAIRNESS

### 2.1 Bias Awareness
⚠️ **Known Biases:**

**1. Semantic Embedding Bias**
- Models trained on internet text
- Internet text contains societal biases
- Embeddings may reflect these biases
- Example: "engineer" associated with male terms historically

**2. Assessment Catalog Bias**
- SHL assessments may have cultural/gender biases
- Not all job types equally represented
- Language preferences embedded in descriptions

**3. Job Description Bias**
- User-provided job titles/skills may be biased
- Gendered language in job descriptions
- Implicit requirements favor certain groups

### 2.2 Mitigation Strategies

✅ **Technical Mitigations:**
```python
1. TRANSPARENCY
   - Show all recommendations
   - Explain matching logic
   - Disclose similarity scores
   - No hidden filtering

2. DIVERSIFICATION
   - Return Top-5, not just Top-1
   - Show range of assessment types
   - Include cognitive and personality tests
   - Multiple pathways to success

3. HUMAN OVERSIGHT
   - Humans review recommendations
   - Final decisions by hiring team
   - No automated decisions
   - Documentation of choices

4. MONITORING
   - Track assessment selection patterns
   - Monitor for adverse impact
   - Regular bias audits
   - Feedback collection
```

✅ **Operational Mitigations:**
```
1. Training
   - Educate recruiters on unconscious bias
   - Review assessment selection process
   - Document hiring decisions
   - Audit outcomes regularly

2. Diverse Hiring Team
   - Multiple perspectives in review
   - Reduce individual biases
   - Cross-check recommendations
   - Collaborative decision-making

3. Standardized Criteria
   - Use consistent job descriptions
   - Avoid subjective language
   - Focus on essential skills
   - Document requirements clearly
```

---

## 3. RESPONSIBLE AI USE

### 3.1 System Limitations

⚠️ **This System CANNOT:**
- ❌ Make hiring decisions automatically
- ❌ Evaluate individual candidates
- ❌ Replace human judgment
- ❌ Guarantee assessment validity
- ❌ Ensure fair hiring outcomes
- ❌ Comply with employment law alone

### 3.2 Appropriate Use Cases

✅ **Recommended Uses:**
1. **Assessment Selection** - Narrowing assessment choices
2. **Process Acceleration** - Speeding up evaluation selection
3. **Learning Tool** - Understanding SHL product offerings
4. **Prototyping** - Exploring new hiring processes
5. **Training** - Teaching about assessment systems

❌ **Prohibited Uses:**
1. **Automated Hiring** - Making final decisions without human review
2. **Sole Assessment** - Only method of candidate evaluation
3. **Bias Amplification** - Using biased job descriptions
4. **Compliance Substitute** - Replacing legal compliance checks
5. **Predictive Hiring** - Predicting future performance

### 3.3 Required Disclaimer

**Every system interaction should display:**

```
⚠️  IMPORTANT DISCLAIMER

This tool recommends SHL assessments based on semantic similarity.

IT IS NOT:
- A hiring tool
- A candidate evaluation tool
- A compliance guarantee
- Legal employment advice
- A bias-free system

IT IS:
- A recommendation system
- For assessment selection only
- A support tool for recruiters
- An educational resource

REQUIRED STEPS:
1. Review all recommendations
2. Consider assessment validity
3. Consult HR/Legal team
4. Document your decisions
5. Monitor outcomes for fairness

NO HIRING DECISIONS should be made
based solely on this system's output.
```

---

## 4. TRANSPARENCY & EXPLAINABILITY

### 4.1 Model Transparency

✅ **Model Used:**
```
Embedding Model: sentence-transformers/all-MiniLM-L6-v2
- Dimensionality: 384
- Training data: STS Benchmark, natural language inference
- Training approach: Supervised learning (public dataset)
- License: MIT (open source)
- Repository: HuggingFace Transformers
```

✅ **How It Works:**
```
1. Takes assessment text
2. Converts to 384-dimensional vector
3. Captures semantic meaning
4. Enables similarity comparison

Math: Cosine similarity between vectors
Range: [-1, 1] where 1 = identical
Display: Converted to similarity score
```

### 4.2 Explainability Features

✅ **What We Show Users:**
```
1. Recommended Assessments
   ✓ Assessment name
   ✓ Similarity score/match percentage
   ✓ Color-coded relevance badge

2. Explanation of Match
   ✓ Which skills are addressed
   ✓ Why this assessment fits the role
   ✓ Experience level alignment

3. Detailed Information
   ✓ Full assessment description
   ✓ Skills measured
   ✓ Job suitability
   ✓ Delivery method
   ✓ Duration

4. Transparency
   ✓ Source: SHL Product Catalog
   ✓ Matching method: Semantic similarity
   ✓ Score calculation: Cosine distance
   ✓ No hidden calculations
```

### 4.3 Interpretability

✅ **Users Can Understand:**
```
Q: Why was this assessment recommended?
A: Shows similarity score and matching skills

Q: How confident is the match?
A: Score percentage (>20% = high confidence)

Q: Can I see the full assessment details?
A: Yes, expandable details with all information

Q: How does the system work?
A: Documentation and code comments explain

Q: Can I trust these recommendations?
A: Yes, grounded in semantic similarity to catalog
```

---

## 5. LEGAL & COMPLIANCE

### 5.1 Regulatory Compliance

⚠️ **Employment Laws:**
- This system does NOT ensure EEOC compliance
- This system does NOT guarantee EEO compliance
- This system does NOT ensure fair hiring practices
- System must be used with legal oversight

✅ **Required Actions:**
```
Before using for actual hiring:
1. Consult employment law attorney
2. Review assessment validity evidence (SHL provides)
3. Conduct adverse impact analysis
4. Implement audit procedures
5. Document all decisions
6. Monitor outcomes regularly
7. Review for bias annually
```

### 5.2 Intellectual Property

✅ **Assessment Data:**
- Source: Public SHL product descriptions
- Usage: Educational/demonstration only
- Ownership: SHL owns assessment IP
- Attribution: SHL assessments referenced

✅ **Open Source Components:**
- sentence-transformers: Apache 2.0 license
- ChromaDB: Apache 2.0 license
- Streamlit: Apache 2.0 license
- All dependencies properly licensed

### 5.3 Data Protection

✅ **GDPR / Privacy Compliance:**
- No personal data collected
- No user profiling
- No data retention
- No third-party sharing
- No cookies/tracking

---

## 6. RESPONSIBLE DEPLOYMENT

### 6.1 For Organizations Using This System

✅ **Best Practices:**

1. **Oversight**
   ```
   - Human review of all recommendations
   - Supervisor approval required
   - Multiple stakeholders involved
   - Clear accountability
   ```

2. **Auditing**
   ```
   - Track which assessments recommended
   - Monitor who received which assessments
   - Analyze hiring outcomes
   - Check for adverse impact
   ```

3. **Feedback**
   ```
   - Collect user feedback
   - Monitor hiring success
   - Adjust assessment selection
   - Iterate and improve
   ```

4. **Training**
   ```
   - Train users on system capabilities
   - Explain limitations clearly
   - Educate on bias risks
   - Document processes
   ```

### 6.2 Ethical Checkpoints

⚠️ **Before Using for Real Hiring:**

- [ ] Legal review completed
- [ ] Bias audit conducted
- [ ] Disclaimer prominently displayed
- [ ] Human review process documented
- [ ] Audit trail established
- [ ] Team trained on limitations
- [ ] Monitoring plan created
- [ ] Feedback mechanism in place

---

## 7. ACCOUNTABILITY & GOVERNANCE

### 7.1 Responsibility Matrix

| Decision | Responsibility |
|----------|-----------------|
| Assessment recommendation | System (advisory) |
| Assessment selection | Human recruiter |
| Candidate evaluation | Human hiring team |
| Hiring decision | Human decision-maker |
| Legal compliance | Organization + Legal team |
| Fairness & ethics | Multiple stakeholders |

### 7.2 Accountability

✅ **System Creators:**
- Provide transparent system
- Document limitations
- Enable auditability
- Support responsible use

✅ **Organization Using System:**
- Implement human oversight
- Maintain audit trail
- Monitor for bias
- Ensure legal compliance
- Document decisions

✅ **Individual Users:**
- Review recommendations critically
- Follow documented processes
- Escalate concerns
- Provide feedback

---

## 8. ONGOING MONITORING

### 8.1 What to Monitor

✅ **Implementation Metrics:**
```
1. Usage patterns
   - Which roles use the system
   - Which assessments recommended
   - Frequency of use

2. Outcome metrics
   - Assessment selection rates
   - Candidate advancement rates
   - Hiring success rates
   - Employee retention

3. Fairness metrics
   - Assessment distribution by demographics
   - Adverse impact ratio
   - Recommendation consistency
   - Score distribution
```

### 8.2 Audit Schedule

✅ **Recommended Frequency:**
```
Monthly:  Usage pattern review
Quarterly: Fairness audit
Annually:  Comprehensive bias assessment
As-needed: Investigation of complaints
```

### 8.3 Escalation Procedures

✅ **If Bias Detected:**
```
1. STOP using system
2. Investigate discrepancy
3. Conduct impact analysis
4. Adjust selection criteria
5. Retrain assessments
6. Resume with modifications
7. Document all actions
```

---

## 9. LIMITATIONS STATEMENT

### 9.1 System Limitations

⚠️ **Technical Limitations:**
- Semantic similarity is not perfect
- May miss non-obvious assessment fits
- Language-dependent (English only)
- Based on historical training data
- No human expertise encoded

⚠️ **Assessment Limitations:**
- SHL assessments not universally applicable
- Validity varies by role and context
- No assessment predicts job success perfectly
- Multiple valid assessment options exist
- Professional judgment required

⚠️ **Fairness Limitations:**
- Semantic similarity can perpetuate biases
- Job descriptions may be biased
- Assessments may have cultural biases
- No system is perfectly fair
- Continuous monitoring essential

### 9.2 What This System Does NOT Do

❌ Cannot:
- Replace professional HR judgment
- Guarantee assessment validity
- Ensure fair hiring
- Evaluate individual candidates
- Predict job performance
- Comply with all employment laws
- Eliminate all bias
- Make hiring decisions

✅ Can:
- Recommend assessments
- Explain matching logic
- Provide transparency
- Support human decision-making
- Accelerate assessment selection
- Enable learning about SHL products

---

## 10. COMMITMENT TO RESPONSIBLE AI

### 10.1 Our Principles

✅ **Transparency**
- Clear about capabilities and limitations
- Explain how system works
- Disclose scores and reasoning
- Open source components

✅ **Fairness**
- Acknowledge bias risks
- Provide diverse recommendations
- Require human oversight
- Enable monitoring and audits

✅ **Accountability**
- Document system behavior
- Enable audit trails
- Maintain clear responsibilities
- Support informed decisions

✅ **Safety**
- Prevent misuse through design
- Require human review
- Disable harmful decisions
- Implement safeguards

### 10.2 Continuous Improvement

✅ **Our Commitment:**
- Monitor system performance
- Gather user feedback
- Improve explanations
- Reduce identified biases
- Update documentation
- Share learnings

---

## 11. DISCLAIMER FOR DEPLOYMENT

### IMPORTANT: READ BEFORE USE

**This system is for educational and assessment selection purposes ONLY.**

#### NOT FOR:
- ❌ Automated hiring decisions
- ❌ Legal employment determinations
- ❌ Sole assessment of candidates
- ❌ Compliance guarantee
- ❌ Bias-free hiring promise

#### IMPORTANT NOTES:
⚠️ All recommendations MUST be reviewed by human hiring professionals
⚠️ No hiring decisions should be made without human judgment
⚠️ Organizations must comply with all employment laws
⚠️ Assessments should be validated for your specific use case
⚠️ This system does not replace professional HR expertise
⚠️ Fairness and compliance are your organization's responsibility
⚠️ Regular bias audits are essential
⚠️ Document all hiring decisions

#### USAGE AGREEMENT:
By using this system, you agree to:
1. Use only for lawful purposes
2. Maintain human oversight
3. Document decision rationale
4. Monitor for adverse impact
5. Comply with all laws
6. Not rely solely on system output
7. Seek legal review if needed
8. Treat as decision support only

---

## 12. CONTACT & SUPPORT

### Questions About:

**System Capabilities:**
- Review SYSTEM_DOCUMENTATION.md
- Check README.md
- Review code comments

**Ethical Concerns:**
- Consult this document
- Seek legal counsel
- Contact SHL directly
- Document concerns

**Implementation Issues:**
- Check error logs
- Review documentation
- Test locally first
- Consult with IT/HR

---

## SIGN-OFF

**Ethics & Compliance Review:** ✅ Completed  
**Responsible AI Principles:** ✅ Confirmed  
**Documentation:** ✅ Complete  
**Limitations:** ✅ Disclosed  

**This system is ready for educational and prototype deployment with proper human oversight and ethical safeguards in place.**

---

**Document Version:** 1.0  
**Last Updated:** December 16, 2025  
**Review Schedule:** Annually or as needed

