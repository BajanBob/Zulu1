plugins { id("com.android.application") }
android {
    namespace = "com.zulu1.hamdogtutor"
    compileSdk = 35
    defaultConfig {
        minSdk = 24
        targetSdk = 35
        versionCode = 2
        versionName = "1.1"
    }
    buildFeatures { resValues = true }
    // One app per student, each with its own name and its own saved progress.
    flavorDimensions += "student"
    productFlavors {
        create("shakai") {
            dimension = "student"
            applicationId = "com.zulu1.hamdogtutor"
            resValue("string", "app_name", "Zulu 1 Ham Dog Tutor")
        }
        create("bubba") {
            dimension = "student"
            applicationId = "com.zulu1.hamdogtutor.bubba"
            resValue("string", "app_name", "Zulu 1 Tutor Bubba")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
