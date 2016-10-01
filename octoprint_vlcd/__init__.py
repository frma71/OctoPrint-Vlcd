# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import octoprint.server

class VlcdPlugin(octoprint.plugin.StartupPlugin,
                 octoprint.plugin.SettingsPlugin,
                 octoprint.plugin.AssetPlugin,
                 octoprint.plugin.SimpleApiPlugin,
                 octoprint.plugin.TemplatePlugin):

	##~~ SettingsPlugin mixin
        def on_after_startup(self):
                self._logger.info("Virtual LCD plugin loaded")
                
	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)
        def on_api_get(self, request):
                self._logger.info("API get:");
                move = request.args.get("move");
                click = request.args.get("click")

                cmd = "M943"
                if not (move == "0"):
                        cmd += (" E" + move);
                if click != "0":
                        cmd += " B4 "
                octoprint.server.printer.commands([cmd])
                
                self._logger.info("Move:" + move);
                self._logger.info("Click:" + click);
                return None
	def hook_actiontrigger(self, comm, line, action_trigger):
                self._logger.info("Action")
                self._logger.info(comm)
                self._logger.info(line)
                self._logger.info(action_trigger)
                lineno=1
                self._plugin_manager.send_plugin_message(self._identifier, dict(lineno=lineno, vlcdtext=action_trigger[4:].replace(".", " ")))
                
        
	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/vlcd.js"],
			css=["css/vlcd.css"],
			less=["less/vlcd.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			vlcd=dict(
				displayName="Virtual LCD",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="frma71",
				repo="OctoPrint-Vlcd",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/frma71/OctoPrint-Vlcd/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Virtual LCD"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = VlcdPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
                'octoprint.comm.protocol.action': __plugin_implementation__.hook_actiontrigger}

