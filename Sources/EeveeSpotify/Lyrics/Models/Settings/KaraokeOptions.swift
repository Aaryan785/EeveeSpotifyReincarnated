import Foundation

enum KaraokeTextAlignment: String, Codable, CaseIterable {
    case leading
    case center
    case trailing

    var displayName: String {
        "karaoke_alignment_\(rawValue)".localized
    }
}

struct KaraokeOptions: Codable, Hashable {
    var textAlignment: KaraokeTextAlignment = .center
    var reversedDirection = false
}
