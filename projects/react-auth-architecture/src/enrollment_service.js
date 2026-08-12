/**
 * Student Enrollment & Domain Logic Service
 * 
 * Handles course registration validations, enforcing capacity constraints,
 * preventing duplicate entries, and applying soft-delete patterns for 
 * data traceability.
 */

class EnrollmentService {
    constructor(dbClient) {
        this.db = dbClient;
    }

    /**
     * Registers a student into a course with strict domain checks.
     */
    async enrollStudent(studentId, courseId) {
        const existingEnrollment = await this.db.query(
            `SELECT id FROM enrollments 
             WHERE student_id = $1 AND course_id = $2 AND is_deleted = false`,
            [studentId, courseId]
        );

        if (existingEnrollment.rows.length > 0) {
            throw new Error('Student is already actively enrolled in this course.');
        }

        const courseQuery = await this.db.query(
            `SELECT max_capacity, 
                (SELECT COUNT(*) FROM enrollments WHERE course_id = $1 AND is_deleted = false) as current_enrolled
             FROM courses WHERE id = $1 AND is_deleted = false`,
            [courseId]
        );

        if (courseQuery.rows.length === 0) {
            throw new Error('Course not found or inactive.');
        }

        const { max_capacity, current_enrolled } = courseQuery.rows[0];

        if (parseInt(current_enrolled, 10) >= max_capacity) {
            throw new Error('Course capacity limit reached.');
        }

        const newEnrollment = await this.db.query(
            `INSERT INTO enrollments (student_id, course_id, enrolled_at, is_deleted)
             VALUES ($1, $2, NOW(), false)
             RETURNING id, student_id, course_id, enrolled_at`,
            [studentId, courseId]
        );

        return newEnrollment.rows[0];
    }

    /**
     * Soft deletes an enrollment record to preserve auditability.
     */
    async softDeleteEnrollment(enrollmentId) {
        const result = await this.db.query(
            `UPDATE enrollments 
             SET is_deleted = true, deleted_at = NOW() 
             WHERE id = $1 AND is_deleted = false
             RETURNING id, is_deleted`,
            [enrollmentId]
        );

        if (result.rows.length === 0) {
            throw new Error('Enrollment record not found or already deleted.');
        }

        return { message: 'Enrollment successfully revoked.', id: enrollmentId };
    }
}

module.exports = EnrollmentService;