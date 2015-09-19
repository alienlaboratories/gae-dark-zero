// Copyright 2015 Alien Laboratories, Inc.

/**
 * Grunt config.
 */
module.exports = function(grunt) {

  grunt.initConfig({

    pkg: grunt.file.readJSON('package.json'),

    // NX project.
    nx: {
      options: {
        virtualenv: 'tools/python'
      }
    }

  });

  // Core tasks
  grunt.task.loadTasks(process.env.GRUNT_TASKS);

  // Targets.
  grunt.registerTask('default', ['nx']);

};
