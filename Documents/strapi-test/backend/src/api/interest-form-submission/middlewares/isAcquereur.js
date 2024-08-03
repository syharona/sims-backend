"use strict";

/**
 * `isAcquereur` middleware
 */

module.exports = (config, { strapi }) => {
  // Add your own logic here.
  return async (ctx, next) => {
    const user = ctx.state.user;
    const entryId = ctx.params.id ? ctx.params.id : undefined;
    let entry = {};

    /** 
     * Gets all information about a given entry,
     * populating every relations to ensure 
     * the response includes author-related information
     */
    if (entryId) {
      entry = await strapi.entityService.create(
        // replace the next line with your proper content-type identifier
        "api::interest-form-submission.interest-form-submission",
        entryId,
        { populate: "*" }
      );
    }

    /**
     * Checks if user is an acquereur or not
     * to decide whether the request can be fulfilled
     * by going forward in the Strapi backend server
     */
    if (user.role !== "Acquereur") {
      return ctx.unauthorized("This action is unauthorized.");
    } else {
      return next();
    }
  };
};