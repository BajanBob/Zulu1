package com.zulu1.hamdogtutor;

import android.app.Activity;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.speech.tts.Voice;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Zulu 1 Ham Dog Tutor: shows the tutor page and speaks with a UK English voice.
 * Uses Google's speech engine when the phone has it, because it pronounces words far better
 * than some phone makers' own engines.
 */
public class MainActivity extends Activity {
    private static final String GOOGLE_TTS = "com.google.android.tts";
    private WebView web;
    private TextToSpeech tts;
    private volatile boolean ready = false;
    private volatile String chosenVoice = "";   // set from Granny Beryl's corner; "" means automatic
    private Voice autoVoice;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        web = new WebView(this);
        setContentView(web);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setAllowFileAccess(true);

        startSpeech(hasGoogleTts() ? GOOGLE_TTS : null);

        web.addJavascriptInterface(new Bridge(), "AndroidTTS");
        web.setWebViewClient(new WebViewClient());
        web.loadUrl("file:///android_asset/index.html");
    }

    private boolean hasGoogleTts() {
        try {
            getPackageManager().getPackageInfo(GOOGLE_TTS, 0);
            return true;
        } catch (PackageManager.NameNotFoundException e) {
            return false;
        }
    }

    private void startSpeech(String engine) {
        TextToSpeech.OnInitListener onInit = status -> {
            if (status == TextToSpeech.SUCCESS) {
                tts.setLanguage(Locale.UK);
                autoVoice = bestFemaleUkVoice();
                ready = true;
                applyVoice(chosenVoice);
            } else if (engine != null) {
                startSpeech(null); // Google engine failed; fall back to the phone's default engine
            }
        };
        tts = engine == null ? new TextToSpeech(this, onInit) : new TextToSpeech(this, onInit, engine);
        tts.setOnUtteranceProgressListener(new UtteranceProgressListener() {
            @Override public void onStart(String id) { }
            @Override public void onDone(String id) { finished(id); }
            @Override public void onError(String id) { finished(id); }
        });
    }

    private List<Voice> ukVoices() {
        List<Voice> out = new ArrayList<>();
        try {
            for (Voice v : tts.getVoices()) {
                if ("GBR".equals(v.getLocale().getISO3Country())) out.add(v);
            }
        } catch (Exception ignored) { }
        return out;
    }

    /** Google's UK voices gba, gbc and gbg are female. */
    private static boolean isFemale(Voice v) {
        String n = v.getName().toLowerCase(Locale.ROOT);
        return n.contains("female") || n.contains("gba") || n.contains("gbc") || n.contains("gbg");
    }

    /** Highest-quality female UK voice that works offline. */
    private Voice bestFemaleUkVoice() {
        Voice best = null;
        for (Voice v : ukVoices()) {
            if (!isFemale(v) || v.isNetworkConnectionRequired()) continue;
            if (best == null || v.getQuality() > best.getQuality()) best = v;
        }
        return best;
    }

    private void applyVoice(String name) {
        if (!ready) return;
        Voice target = autoVoice;
        if (name != null && !name.isEmpty()) {
            for (Voice v : ukVoices()) if (v.getName().equals(name)) { target = v; break; }
        }
        try {
            if (target != null) tts.setVoice(target); else tts.setLanguage(Locale.UK);
        } catch (Exception ignored) { }
    }

    private void finished(String id) {
        runOnUiThread(() -> web.evaluateJavascript(
                "window.__ttsDone&&window.__ttsDone('" + id.replace("'", "") + "')", null));
    }

    private class Bridge {
        @JavascriptInterface
        public void speak(String text, float rate, boolean flush, String id) {
            if (tts == null || !ready) { finished(id); return; }
            tts.setSpeechRate(rate);
            tts.setPitch(1.0f);
            tts.speak(text, flush ? TextToSpeech.QUEUE_FLUSH : TextToSpeech.QUEUE_ADD, null, id);
        }

        @JavascriptInterface
        public void stop() {
            if (tts != null) tts.stop();
        }

        /** UK voices on this phone as JSON, for the voice samples list. */
        @JavascriptInterface
        public String voices() {
            JSONArray arr = new JSONArray();
            if (!ready) return "loading"; // the page shows a simple sample button until voices are ready
            String auto = autoVoice == null ? "" : autoVoice.getName();
            for (Voice v : ukVoices()) {
                try {
                    JSONObject o = new JSONObject();
                    o.put("name", v.getName());
                    o.put("female", isFemale(v));
                    o.put("online", v.isNetworkConnectionRequired());
                    o.put("quality", v.getQuality());
                    o.put("auto", v.getName().equals(auto));
                    arr.put(o);
                } catch (Exception ignored) { }
            }
            return arr.toString();
        }

        @JavascriptInterface
        public String engine() {
            return tts == null ? "" : String.valueOf(tts.getDefaultEngine());
        }

        @JavascriptInterface
        public boolean googleEngine() {
            return hasGoogleTts();
        }

        /** Choose Zulu's voice by name; "" goes back to automatic. */
        @JavascriptInterface
        public void useVoice(String name) {
            chosenVoice = name == null ? "" : name;
            applyVoice(chosenVoice);
        }

        /** Play a sample in one voice, then go back to Zulu's chosen voice. */
        @JavascriptInterface
        public void sample(String text, float rate, String name) {
            if (tts == null || !ready) return;
            applyVoice(name);
            tts.setSpeechRate(rate);
            tts.setPitch(1.0f);
            tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "sample");
            applyVoice(chosenVoice);
        }
    }

    @Override
    protected void onDestroy() {
        if (tts != null) { tts.stop(); tts.shutdown(); }
        web.destroy();
        super.onDestroy();
    }
}
