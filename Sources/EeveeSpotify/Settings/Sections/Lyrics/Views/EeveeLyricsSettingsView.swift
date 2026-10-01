import SwiftUI

struct EeveeLyricsSettingsView: View {
    @StateObject var viewModel = EeveeLyricsSettingsViewModel()
    @State private var karaokeOptions: KaraokeOptions = UserDefaults.karaokeOptions
    @State private var spicyLyricsApiKey: String = UserDefaults.spicyLyricsApiKey

    var body: some View {
        List {
            lyricsSourceSection()
            
            if viewModel.lyricsSource != .notReplaced {
                if viewModel.lyricsSource != .genius {
                    geniusFallbackSection()
                }
                
                hideOnErrorSection()
                romanizedLyricsSection()
                
                if viewModel.lyricsSource == .musixmatch {
                    musixmatchLanguageSection()
                }

                if viewModel.lyricsSource == .spicylyrics {
                    spicyLyricsApiKeySection()
                    karaokeAppearanceSection()
                    SettingsResetSection(visible: karaokeOptions != KaraokeOptions()) { karaokeOptions = KaraokeOptions() }
                }
            }

            SpacerView()
        }
        .onReceive(viewModel.musixmatchTokenInputAlertPublisher) { showAnonymousTokenOption in
            showMusixmatchTokenAlert(UserDefaults.lyricsSource, showAnonymousTokenOption)
        }
        .eeveeSettingsStyle()
        .disabled(viewModel.isRequestingMusixmatchToken)
        .animation(.default, value: viewModel.animationValues)
        .onChange(of: karaokeOptions) { UserDefaults.karaokeOptions = $0 }
        .onChange(of: spicyLyricsApiKey) { UserDefaults.spicyLyricsApiKey = $0 }
    }

    @ViewBuilder private func spicyLyricsApiKeySection() -> some View {
        Section {
            TextField("spicylyrics_api_key_placeholder".localized, text: $spicyLyricsApiKey)
                .autocapitalization(.none)
                .disableAutocorrection(true)
        } header: {
            Text("spicylyrics_api_key".localized)
        } footer: {
            Text("spicylyrics_api_key_description".localized)
        }
    }

    @ViewBuilder private func karaokeAppearanceSection() -> some View {
        Section {
            Picker("karaoke_alignment".localized, selection: $karaokeOptions.textAlignment) {
                ForEach(KaraokeTextAlignment.allCases, id: \.self) { alignment in
                    Text(alignment.displayName).tag(alignment)
                }
            }

            Toggle(
                "karaoke_reversed_direction".localized,
                isOn: $karaokeOptions.reversedDirection
            )
        } header: {
            Text("karaoke_section".localized)
        } footer: {
            Text("karaoke_section_footer".localized)
        }
    }
    
    @ViewBuilder private func geniusFallbackSection() -> some View {
        Section {
            Toggle(
                "genius_fallback".localized,
                isOn: $viewModel.lyricsOptions.geniusFallback
            )
            
            if viewModel.lyricsOptions.geniusFallback {
                Toggle(
                    "show_fallback_reasons".localized,
                    isOn: $viewModel.lyricsOptions.showFallbackReasons
                )
            }
        } footer: {
            Text("genius_fallback_description"
                .localizeWithFormat(viewModel.lyricsSource.description))
        }
    }
    
    @ViewBuilder private func romanizedLyricsSection() -> some View {
        Section {
            Toggle(
                "romanized_lyrics".localized,
                isOn: $viewModel.lyricsOptions.romanization
            )
        } footer: {
            Text("romanized_lyrics_description".localized)
        }
    }
    
    @ViewBuilder private func hideOnErrorSection() -> some View {
        Section {
            Toggle(
                "hide_lyrics_on_error".localized,
                isOn: $viewModel.lyricsOptions.hideOnError
            )
        } footer: {
            Text("hide_lyrics_on_error_description".localized)
        }
    }
    
    @ViewBuilder private func musixmatchLanguageSection() -> some View {
        Section {
            HStack {
                Text("musixmatch_language".localized)
                
                Spacer()
                
                TextField("en", text: $viewModel.lyricsOptions.musixmatchLanguage)
                    .frame(maxWidth: 20)
                    .foregroundColor(.gray)
            }
            .icon(
                "exclamationmark.triangle.fill",
                color: .yellow,
                when: $viewModel.showMusixmatchInvalidLanguageWarning
            )
        } footer: {
            Text("musixmatch_language_description".localized)
        }
    }
}
