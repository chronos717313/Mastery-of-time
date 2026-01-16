# Zenodo Upload Instructions

**Step-by-Step Guide to Publishing TMT Dataset on Zenodo**

---

## 📋 Prerequisites

- [ ] Zenodo account created (https://zenodo.org/)
- [ ] ORCID linked to Zenodo account (recommended)
- [ ] All files in `zenodo_package/` ready for upload
- [ ] GitHub repository public (for integration)

---

## 🚀 Upload Process

### Step 1: Create New Upload

1. Go to https://zenodo.org/
2. Click **"New upload"** (top right, or + button)
3. You'll see the upload form

### Step 2: Upload Files

**Option A: Drag & Drop**
- Drag the entire `zenodo_package/` folder into the upload area

**Option B: Manual Upload**
- Click "Choose files"
- Select all 18 files from `zenodo_package/`:
  ```
  ✓ README_ZENODO.md
  ✓ QUICK_START_GUIDE.md
  ✓ MANIFEST.txt
  ✓ METADATA.json
  ✓ LICENSE
  ✓ CITATION.cff
  ✓ ZENODO_UPLOAD_INSTRUCTIONS.md (this file)
  ✓ CORE_CONCEPTS.md
  ✓ DARK_MATTER_DEFINITION.md
  ✓ DARK_ENERGY_DEFINITION.md
  ✓ COMPLETE_MATHEMATICAL_FORMULATION_MT.md
  ✓ FORMALIZATION_H_Z_RHO.md
  ✓ LEXICON_DESPRES_MASS_AND_MAPPING.md
  ✓ FINAL_SUMMARY_WEAK_LENSING_TEST_TMT.md
  ✓ WEAK_LENSING_TEST_EXECUTION_REPORT.md
  ✓ COSMOS_DES_DOWNLOAD_GUIDE.md
  ✓ COSMOS_DES_TEST_GUIDE.md
  ✓ UNIQUE_TESTABLE_PREDICTION.md
  ✓ SCIENTIFIC_ARTICLE_TIME_MASTERY.md
  ✓ FIGURE_SPECIFICATIONS.md
  ```

**Total**: 20 files, ~180 KB

### Step 3: Fill Metadata

#### Basic Information

**Upload type**: Dataset

**Publication date**: 2026-01-15

**Title**:
```
Time Mastery Theory: Alternative Cosmological Framework via Temporal Distortion
```

**Authors**:
```
Després Asselin, Pierre-Olivier
Affiliation: Independent Researcher
ORCID: [your ORCID if you have one]
```

#### Description

Paste from `METADATA.json` or use:

```
The Time Mastery Theory (TMT) proposes an alternative explanation for dark matter and dark energy through geometric effects in spacetime. This dataset includes complete documentation, mathematical formulation, and experimental validation methodology for the decisive weak lensing test.

Key result: Universal law k(M_bary, f_gas) with R²=0.9976 over 10,000+ galaxies.

Current status: Methodology validated, awaiting real COSMOS/DES data for decisive test.

The theory predicts dark matter halo alignment with neighbors (r>0.50), testable with COSMOS/DES weak lensing surveys. Current simulation (N=5,000) shows r=0.378 [0.357, 0.399], p<10⁻⁸⁸.

Timeline: 4-6 months to decisive result with real observational data.
```

**Version**: v0.4.0-beta

**Language**: English

#### License

**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)

**Access right**: Open Access

#### Keywords (Add all)

```
cosmology
dark matter
dark energy
alternative theory
weak gravitational lensing
temporal distortion
general relativity
galaxy rotation curves
ΛCDM alternative
geometric dark matter
universal law
COSMOS survey
DES survey
falsifiable prediction
time dilation
spacetime curvature
```

#### Subjects (Select)

```
- Astrophysics - Cosmology and Nongalactic Astrophysics (astro-ph.CO)
- General Relativity and Quantum Cosmology (gr-qc)
```

#### Additional Information

**Notes**:
```
This work presents a falsifiable alternative to the ΛCDM cosmological model. The theory predicts a specific correlation r>0.50 for dark matter halo alignment with neighboring galaxies, testable with COSMOS/DES weak lensing data.

Current simulation results (N=5,000) show r=0.378 [0.357, 0.399] with p<10⁻⁸⁸, demonstrating methodology validity while requiring real observational data for decisive test.

Repository: https://github.com/cadespres/Maitrise-du-temps
```

#### Related Identifiers

**GitHub Repository**:
```
Identifier: https://github.com/cadespres/Maitrise-du-temps
Relation: is supplemented by
Resource type: Software
```

#### References

Add these key references:
```
Bartelmann & Schneider (2001). Weak gravitational lensing. Physics Reports, 340, 291-472.

DES Collaboration (2021). Dark Energy Survey Year 3 results. ApJS, 254, 24.

Scoville et al. (2007). The Cosmic Evolution Survey (COSMOS). ApJS, 172, 1.

Kilbinger (2015). Cosmology with cosmic shear observations. Reports on Progress in Physics, 78, 086901.
```

#### Contributors (Optional)

You can acknowledge:
```
COSMOS Team (Data Collector) - Caltech/JPL
DES Collaboration (Data Collector) - Dark Energy Survey
```

### Step 4: Pre-Publish Review

Before clicking "Publish":

- [ ] All 20 files uploaded successfully
- [ ] Title correct and complete
- [ ] Description clear and accurate
- [ ] Keywords comprehensive
- [ ] License set to CC BY 4.0
- [ ] GitHub repository linked
- [ ] References added

### Step 5: Publish!

1. Click **"Publish"** button
2. Zenodo will assign a **permanent DOI**
3. DOI format: `10.5281/zenodo.XXXXXXX`

### Step 6: Update Files with Real DOI

Once published, you'll get a real DOI. Update these files:

1. **README_ZENODO.md** - Replace `10.5281/zenodo.XXXXXXX` with real DOI
2. **CITATION.cff** - Update DOI field
3. **LICENSE** - Update citation DOI
4. **GitHub README.md** - Add Zenodo badge

**Zenodo badge code**:
```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
```

### Step 7: Create New Version (If Needed)

To update the dataset later:

1. Go to your Zenodo record
2. Click "New version"
3. Upload updated files
4. Zenodo creates new DOI (versioned)
5. Old version remains accessible

---

## 🔗 After Publishing

### Update GitHub

Add to main README.md:
```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
```

### Share on Social Media

Twitter/X template:
```
🚀 New dataset published!

Time Mastery Theory: Alternative explanation for dark matter/energy via temporal distortion geometry.

✅ Universal law k(M,fgas) R²=0.9976
🔬 Decisive test ready (4-6 months)
📊 r=0.378 [0.357,0.399], p<10⁻⁸⁸

https://doi.org/10.5281/zenodo.XXXXXXX

#cosmology #darkmatter #science
```

### Notify Relevant Communities

Consider sharing with:
- r/cosmology (Reddit)
- r/Physics (Reddit)
- arXiv mailing lists
- DES Collaboration
- COSMOS Team

---

## 📧 Support

If you encounter issues:

**Zenodo Support**: https://zenodo.org/support
**Email**: info@zenodo.org

**TMT Contact**: pierreolivierdespres@gmail.com

---

## ✅ Checklist

Before upload:
- [ ] All files reviewed and finalized
- [ ] Metadata prepared
- [ ] GitHub repository public
- [ ] ORCID account (optional but recommended)

During upload:
- [ ] Files uploaded (20 files)
- [ ] Metadata filled completely
- [ ] License selected (CC BY 4.0)
- [ ] Keywords added
- [ ] References added

After publish:
- [ ] DOI received
- [ ] Files updated with real DOI
- [ ] GitHub README updated with badge
- [ ] Social media announcement

---

## 🎉 Congratulations!

Your TMT dataset is now:
- ✅ Permanently archived
- ✅ Citable with DOI
- ✅ Discoverable worldwide
- ✅ Open Access (CC BY 4.0)

---

**Ready to upload!** 🚀

*Package size: ~180 KB*
*Upload time: ~5-10 minutes*
*Impact: Potentially revolutionary* 🌟
