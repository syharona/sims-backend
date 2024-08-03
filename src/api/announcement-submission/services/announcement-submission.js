'use strict';

/**
 * announcement-submission service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::announcement-submission.announcement-submission');
