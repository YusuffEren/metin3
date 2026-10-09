#ifndef METIN2MOBILE_RECONSTRUCTED_PROTOCOL_H
#define METIN2MOBILE_RECONSTRUCTED_PROTOCOL_H

/* Clean-room protocol notes reconstructed from the ARM64 client.
 * This is not an original project header.  Structures are byte packed.
 */
#include <stdint.h>

#if defined(_MSC_VER)
#  pragma pack(push, 1)
#  define M2_PACKED
#else
#  define M2_PACKED __attribute__((packed))
#endif

enum M2Phase {
    M2_PHASE_OFFLINE = 0,
    M2_PHASE_HANDSHAKE = 1,
    M2_PHASE_LOGIN = 2,
    M2_PHASE_SELECT = 3,
    M2_PHASE_LOADING = 4,
    M2_PHASE_GAME = 5
};

enum M2Header {
    M2_CG_LOGIN = 0x01,
    M2_CG_ATTACK = 0x02,
    M2_CG_CREATE_CHARACTER = 0x04,
    M2_CG_DESTROY_CHARACTER = 0x05,
    M2_CG_SELECT_CHARACTER = 0x06,
    M2_GC_LOGIN_FAILURE = 0x07,
    M2_GC_CREATE_SUCCESS = 0x08,
    M2_CG_DIRECT_ENTER = 0x09,
    M2_CG_ENTER_GAME = 0x0A,
    M2_CG_ITEM_DROP = 0x0C,
    M2_CG_ITEM_MOVE = 0x0D,
    M2_CG_ITEM_PICKUP = 0x0F,
    M2_CG_ITEM_DROP_NEW = 0x14,
    M2_CG_ITEM_DELETE = 0x15,
    M2_CG_ITEM_SELL = 0x16,
    M2_GC_LOGIN_SUCCESS_4 = 0x20,
    M2_GC_PING = 0x2C,
    M2_CG_ITEM_USE_TO_ITEM = 0x3C,
    M2_CG_SELECT_EMPIRE = 0x5A,
    M2_CG_CHANGE_NAME = 0x6A,
    M2_GC_CHANGE_NAME_RESULT = 0x6B,
    M2_CG_CHINA_MATRIX_CARD = 0x6C,
    M2_CG_LOGIN_NEW = 0x6D,
    M2_GC_LOGIN_KEY = 0x76,
    M2_CG_RUNUP_MATRIX_ANSWER = 0xC9,
    M2_CG_PASSPOD_ANSWER = 0xCA,
    M2_GC_KEY_AGREEMENT_DONE = 0xFA,
    M2_GC_KEY_AGREEMENT = 0xFB,
    M2_GC_PHASE = 0xFD,
    M2_CG_PONG = 0xFE,
    M2_GC_HANDSHAKE = 0xFF
};

typedef struct M2_PACKED {
    uint8_t header;
    uint32_t handshake;
    uint32_t time_ms;
    int32_t delta;
} M2HandshakePacket;

typedef struct M2_PACKED {
    uint8_t header;
    uint8_t phase;
} M2PhasePacket;

typedef struct M2_PACKED {
    uint8_t header;
    char login[31];
    char password[17];
} M2LoginPacket;

typedef struct M2_PACKED {
    uint8_t header;
    char login[31];
    uint32_t login_key;
    uint8_t encrypt_key[16];
} M2LoginNewPacket;

typedef struct M2_PACKED {
    uint8_t header;
    uint8_t attack_type;
    uint32_t victim_vid;
    uint8_t check_a;
    uint8_t check_b;
} M2AttackPacket;

typedef struct M2_PACKED {
    uint16_t cell;
    uint8_t window_type;
} M2ItemPos;

#if defined(_MSC_VER)
#  pragma pack(pop)
#endif

#if defined(__cplusplus)
static_assert(sizeof(M2HandshakePacket) == 13, "M2HandshakePacket layout mismatch");
static_assert(sizeof(M2PhasePacket) == 2, "M2PhasePacket layout mismatch");
static_assert(sizeof(M2LoginPacket) == 49, "M2LoginPacket layout mismatch");
static_assert(sizeof(M2LoginNewPacket) == 52, "M2LoginNewPacket layout mismatch");
static_assert(sizeof(M2AttackPacket) == 8, "M2AttackPacket layout mismatch");
static_assert(sizeof(M2ItemPos) == 3, "M2ItemPos layout mismatch");
#endif

#endif
