/**
 * Diploma & Certificate Generation Service
 * 
 * Compiles dynamic Handlebars HTML templates using database records 
 * and renders PDF documents in headless Chrome via Puppeteer.
 */

const handlebars = require('handlebars');
const puppeteer = require('puppeteer');
const fs = require('fs-extra');
const path = require('path');

const generateDiplomaPDF = async (studentData, courseData) => {
    const templatePath = path.join(__dirname, '../templates/diploma.hbs');
    const templateHtml = await fs.readFile(templatePath, 'utf8');

    const compileTemplate = handlebars.compile(templateHtml);
    const htmlContent = compileTemplate({
        studentName: studentData.fullName,
        courseName: courseData.title,
        completionDate: new Date().toLocaleDateString(),
        issueId: studentData.enrollmentId
    });

    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    
    await page.setContent(htmlContent, { waitUntil: 'networkidle0' });
    const pdfBuffer = await page.pdf({
        format: 'A4',
        landscape: true,
        printBackground: true
    });

    await browser.close();
    return pdfBuffer;
};

module.exports = { generateDiplomaPDF };