import UIKit
import WebKit
import AVFoundation

/// Zulu 1 Ham Dog Tutor for iPhone and iPad: shows the tutor page and speaks with a UK English voice.
@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    var window: UIWindow?

    func application(_ application: UIApplication,
                     didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        // Play sound even when the silent switch is on.
        try? AVAudioSession.sharedInstance().setCategory(.playback, mode: .spokenAudio, options: [.mixWithOthers])
        try? AVAudioSession.sharedInstance().setActive(true)
        window = UIWindow(frame: UIScreen.main.bounds)
        window?.rootViewController = TutorViewController()
        window?.makeKeyAndVisible()
        return true
    }
}

final class TutorViewController: UIViewController, WKScriptMessageHandler, AVSpeechSynthesizerDelegate {
    private var web: WKWebView!
    private let synth = AVSpeechSynthesizer()
    private var ids: [ObjectIdentifier: String] = [:]
    private lazy var voice: AVSpeechSynthesisVoice? = Self.pickUkFemaleVoice()

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = UIColor(red: 1, green: 0.97, blue: 0.9, alpha: 1)
        synth.delegate = self

        let config = WKWebViewConfiguration()
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []
        let bridge = """
        window.AndroidTTS = {
          speak: function(t, r, f, id) { window.webkit.messageHandlers.tts.postMessage({cmd: 'speak', text: String(t), rate: r, flush: f, id: id}); },
          stop: function() { window.webkit.messageHandlers.tts.postMessage({cmd: 'stop'}); }
        };
        """
        config.userContentController.addUserScript(
            WKUserScript(source: bridge, injectionTime: .atDocumentStart, forMainFrameOnly: true))
        config.userContentController.add(self, name: "tts")

        web = WKWebView(frame: view.bounds, configuration: config)
        web.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        web.isOpaque = false
        web.backgroundColor = view.backgroundColor
        view.addSubview(web)

        if let url = Bundle.main.url(forResource: "index", withExtension: "html") {
            web.loadFileURL(url, allowingReadAccessTo: url.deletingLastPathComponent())
        }
    }

    private static func pickUkFemaleVoice() -> AVSpeechSynthesisVoice? {
        let uk = AVSpeechSynthesisVoice.speechVoices().filter { $0.language == "en-GB" }
        let female = uk.filter { $0.gender == .female }
        // Best quality first: premium, then enhanced, then default.
        let best = female.max { $0.quality.rawValue < $1.quality.rawValue }
        return best ?? uk.max { $0.quality.rawValue < $1.quality.rawValue } ?? AVSpeechSynthesisVoice(language: "en-GB")
    }

    func userContentController(_ controller: WKUserContentController, didReceive message: WKScriptMessage) {
        guard let body = message.body as? [String: Any], let cmd = body["cmd"] as? String else { return }
        if cmd == "stop" {
            synth.stopSpeaking(at: .immediate)
            return
        }
        guard let text = body["text"] as? String else { return }
        let id = body["id"] as? String ?? ""
        if (body["flush"] as? Bool) == true { synth.stopSpeaking(at: .immediate) }
        let rate = (body["rate"] as? Double) ?? 0.9
        let u = AVSpeechUtterance(string: text)
        u.voice = voice
        u.rate = Float(Double(AVSpeechUtteranceDefaultSpeechRate) * rate)
        u.pitchMultiplier = 1.0
        ids[ObjectIdentifier(u)] = id
        synth.speak(u)
    }

    private func finished(_ u: AVSpeechUtterance) {
        guard let id = ids.removeValue(forKey: ObjectIdentifier(u)) else { return }
        let safe = id.replacingOccurrences(of: "'", with: "")
        web.evaluateJavaScript("window.__ttsDone && window.__ttsDone('\(safe)')", completionHandler: nil)
    }

    func speechSynthesizer(_ s: AVSpeechSynthesizer, didFinish u: AVSpeechUtterance) { finished(u) }
    func speechSynthesizer(_ s: AVSpeechSynthesizer, didCancel u: AVSpeechUtterance) { finished(u) }
}
