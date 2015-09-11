/*添加插件*/
/*Connection Plugin*/
cordova plugin add https://git-wip-us.apache.org/repos/asf/cordova-plugin-network-information.git
/*Android*/
(in app/res/xml/config.xml)
<feature name="NetworkStatus">
    <param name="android-package" value="org.apache.cordova.NetworkManager" />
</feature>
(in app/AndroidManifest.xml)
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

/*Camera Plugin*/
cordova plugin add org.apache.cordova.camera

/*Action Sheet Plugin*/
cordova plugin add https://github.com/EddyVerbruggen/cordova-plugin-actionsheet.git

/*Toast Plugin*/
cordova plugin add https://github.com/EddyVerbruggen/Toast-PhoneGap-Plugin.git

/*App Version Plugin*/
cordova plugin add https://github.com/whiteoctober/cordova-plugin-app-version.git

