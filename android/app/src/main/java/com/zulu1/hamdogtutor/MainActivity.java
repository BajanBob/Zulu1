package com.zulu1.hamdogtutor;

import android.app.Activity;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.speech.tts.Voice;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import java.util.Locale;

/** Zulu 1 Ham Dog Tutor: shows the tutor page and speaks with the phone's UK English voice. */
public class MainActivity extends Activity {
    private WebView web;
    private TextToSpeech tts;

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

        tts = new TextToSpeech(this, status -> {
            if (status == TextToSpeech.SUCCESS) {
                tts.setLanguage(Locale.UK);
                pickFemaleUkVoice();
            }
        });
        tts.setOnUtteranceProgressListener(new UtteranceProgressListener() {
            @Override public void onStart(String id) { }
            @Override public void onDone(String id) { finished(id); }
            @Override public void onError(String id) { finished(id); }
        });

        web.addJavascriptInterface(new Bridge(), "AndroidTTS");
        web.setWebViewClient(new WebViewClient());
        web.loadUrl("file:///android_asset/index.html");
    }

    /** Google's UK voices gba, gbc and gbg are female; pick the highest-quality offline one. */
    private void pickFemaleUkVoice() {
        try {
            Voice best = null;
            for (Voice v : tts.getVoices()) {
                if (!"GBR".equals(v.getLocale().getISO3Country())) continue;
                String n = v.getName().toLowerCase(Locale.ROOT);
                boolean female = n.contains("female") || n.contains("gba") || n.contains("gbc") || n.contains("gbg");
                if (!female || v.isNetworkConnectionRequired()) continue;
                if (best == null || v.getQuality() > best.getQuality()) best = v;
            }
            if (best != null) tts.setVoice(best);
        } catch (Exception ignored) { }
    }

    private void finished(String id) {
        runOnUiThread(() -> web.evaluateJavascript(
                "window.__ttsDone&&window.__ttsDone('" + id.replace("'", "") + "')", null));
    }

    private class Bridge {
        @JavascriptInterface
        public void speak(String text, float rate, boolean flush, String id) {
            if (tts == null) { finished(id); return; }
            tts.setSpeechRate(rate);
            tts.setPitch(1.0f);
            tts.speak(text, flush ? TextToSpeech.QUEUE_FLUSH : TextToSpeech.QUEUE_ADD, null, id);
        }

        @JavascriptInterface
        public void stop() {
            if (tts != null) tts.stop();
        }
    }

    @Override
    protected void onDestroy() {
        if (tts != null) { tts.stop(); tts.shutdown(); }
        web.destroy();
        super.onDestroy();
    }
}
