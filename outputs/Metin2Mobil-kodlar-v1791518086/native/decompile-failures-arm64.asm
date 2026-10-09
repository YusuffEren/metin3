; Assembly fallback for five functions not lifted by Ghidra

; ============================================================
; jpeg_load @ 0078b134
; body=[[0078b134, 0078b433] [0078bb58, 0078bbe3] [0078bc0c, 0078bc0f]]
; ============================================================
0078b134  str d14,[sp, #-0xa0]!
0078b138  stp d13,d12,[sp, #0x10]
0078b13c  stp d11,d10,[sp, #0x20]
0078b140  stp d9,d8,[sp, #0x30]
0078b144  stp x29,x30,[sp, #0x40]
0078b148  stp x28,x27,[sp, #0x50]
0078b14c  stp x26,x25,[sp, #0x60]
0078b150  stp x24,x23,[sp, #0x70]
0078b154  stp x22,x21,[sp, #0x80]
0078b158  stp x20,x19,[sp, #0x90]
0078b15c  add x29,sp,#0x40
0078b160  sub sp,sp,#0x530
0078b164  mrs x19,tpidr_el0
0078b168  mov x26,x1
0078b16c  ldr x8,[x19, #0x28]
0078b170  adrp x1,0x38f000
0078b174  add x1,x1,#0x94a
0078b178  mov x22,x3
0078b17c  mov x23,x2
0078b180  mov x21,x0
0078b184  stur x8,[x29, #-0x50]
0078b188  bl 0x00d15100
0078b18c  cbz x0,0x0078bbc0
0078b190  mov x20,x0
0078b194  add x0,sp,#0x200
0078b198  str x19,[sp, #0xd0]
0078b19c  bl 0x00d20070
0078b1a0  str x0,[sp, #0x2a8]
0078b1a4  add x0,sp,#0x2a8
0078b1a8  mov w1,#0x5a
0078b1ac  mov w2,#0x278
0078b1b0  bl 0x00d20120
0078b1b4  add x0,sp,#0x2a8
0078b1b8  mov x1,x20
0078b1bc  str x20,[sp, #0xc8]
0078b1c0  bl 0x00d20180
0078b1c4  add x0,sp,#0x2a8
0078b1c8  mov w1,#0x1
0078b1cc  bl 0x00d20130
0078b1d0  add x0,sp,#0x2a8
0078b1d4  bl 0x00d20140
0078b1d8  ldrsw x19,[sp, #0x31c]
0078b1dc  lsl w24,w19,#0x2
0078b1e0  mov x0,x24
0078b1e4  bl 0x00d16320
0078b1e8  ldr w20,[sp, #0x320]
0078b1ec  str x0,[sp, #0x108]
0078b1f0  str w19,[x23]
0078b1f4  mul w8,w24,w20
0078b1f8  str w20,[x22]
0078b1fc  sxtw x0,w8
0078b200  bl 0x00d16320
0078b204  cmp w20,#0x1
0078b208  str x20,[sp, #0x100]
0078b20c  str x0,[x26]
0078b210  b.lt 0x0078bb58
0078b214  and x10,x19,#0xffffffff
0078b218  mov w9,#0x10
0078b21c  lsl x8,x10,#0x2
0078b220  add x11,x19,x19, LSL #0x1
0078b224  and x15,x19,#0x7
0078b228  and x12,x10,#0xfffffff8
0078b22c  movi v0.2D,#-0x1
0078b230  str x10,[sp, #0xe8]
0078b234  str x8,[sp, #0xd8]
0078b238  add x8,x10,x10, LSL #0x1
0078b23c  sub x8,x8,#0x1
0078b240  lsl x14,x19,#0x2
0078b244  movi v8.2D,#-0x1
0078b248  mov x16,x19
0078b24c  mov x22,xzr
0078b250  mov x23,xzr
0078b254  str x8,[sp, #0xb8]
0078b258  and x8,x10,#0xfffffff0
0078b25c  str x12,[sp, #0xb0]
0078b260  neg x12,x12
0078b264  sub x25,x14,#0x40
0078b268  sub x21,x14,#0x20
0078b26c  str x8,[sp, #0xa0]
0078b270  ands x8,x10,#0xf
0078b274  csel x13,x9,x8,eq
0078b278  ands x8,x10,#0x7
0078b27c  mov w9,#0x8
0078b280  mov x27,#-0x4
0078b284  csel x8,x9,x8,eq
0078b288  mov w20,#0x40
0078b28c  str x13,[sp, #0x20]
0078b290  sub x13,x10,x13
0078b294  sub x9,x10,x8
0078b298  sub x8,x8,x10
0078b29c  mov w28,#0x3
0078b2a0  mov w24,#0xff
0078b2a4  str x12,[sp, #0xa8]
0078b2a8  stp x9,x13,[sp, #0x50]
0078b2ac  and x9,x19,#-0x10
0078b2b0  and x13,x10,#0xffffffe0
0078b2b4  str x14,[sp, #0x148]
0078b2b8  str x11,[sp, #0xc0]
0078b2bc  str x9,[sp, #0x98]
0078b2c0  and x9,x19,#0xf
0078b2c4  str x13,[sp, #0x90]
0078b2c8  and x13,x10,#0x18
0078b2cc  add x10,sp,#0x1b0
0078b2d0  str x26,[sp, #0xe0]
0078b2d4  str x9,[sp, #0x10]
0078b2d8  and x9,x19,#-0x8
0078b2dc  str x13,[sp, #0x8]
0078b2e0  st1 {v0.2D,v1.2D,v2.2D,v3.2D},[x10]
0078b2e4  adrp x10,0x3b1000
0078b2e8  ldr q27,[x10, #0x540]
0078b2ec  adrp x10,0x3b0000
0078b2f0  stp x9,x8,[sp, #0x40]
0078b2f4  sub x8,x11,#0x30
0078b2f8  ldr q30,[x10, #0xa50]
0078b2fc  mov w10,#0x1c7
0078b300  str x8,[sp, #0x18]
0078b304  sub x8,x11,#0x18
0078b308  str q27,[sp, #0xf0]
0078b30c  str q30,[sp, #0x1a0]
0078b310  stp x8,x15,[sp, #0x30]
0078b314  neg x8,x9
0078b318  adrp x9,0x3b1000
0078b31c  str x8,[sp, #0x28]
0078b320  adrp x8,0x3b2000
0078b324  ldr q26,[x9, #0x160]
0078b328  adrp x9,0x3b0000
0078b32c  ldr q0,[x8, #0xe0]
0078b330  adrp x8,0x3b0000
0078b334  ldr q29,[x9, #0xa40]
0078b338  mov w9,#0x10f
0078b33c  ldr q28,[x8, #0xcf0]
0078b340  mov w8,#0x168
0078b344  str q0,[sp, #0x190]
0078b348  dup v0.4S,w9
0078b34c  str q29,[sp, #0x110]
0078b350  dup v1.4S,w8
0078b354  stp q28,q26,[sp, #0x120]
0078b358  stp q0,q1,[sp, #0x70]
0078b35c  dup v0.4S,w10
0078b360  str q0,[sp, #0x60]
0078b364  b 0x0078b398
0078b368  ldr x8,[sp, #0x148]
0078b36c  add x23,x23,#0x1
0078b370  ldr x26,[sp, #0xe0]
0078b374  add x22,x22,x8
0078b378  add x25,x25,x8
0078b37c  add x21,x21,x8
0078b380  add x27,x27,x8
0078b384  add x20,x20,x8
0078b388  add x28,x28,x8
0078b38c  ldr x8,[sp, #0x100]
0078b390  cmp x23,x8
0078b394  b.eq 0x0078bb58
0078b398  add x8,sp,#0x1b0
0078b39c  add x0,sp,#0x2a8
0078b3a0  add x1,sp,#0x1f8
0078b3a4  mov w2,#0x1
0078b3a8  ldr x19,[x26]
0078b3ac  mov x26,x16
0078b3b0  ld1 {v0.2D,v1.2D,v2.2D,v3.2D},[x8]
0078b3b4  add x8,sp,#0x1b0
0078b3b8  st1 {v0.2D,v1.2D,v2.2D,v3.2D},[x8]
0078b3bc  add x8,sp,#0x150
0078b3c0  st1 {v8.2D,v9.2D,v10.2D,v11.2D},[x8]
0078b3c4  ldr x8,[sp, #0x108]
0078b3c8  str x8,[sp, #0x1f8]
0078b3cc  bl 0x00d20150
0078b3d0  add x8,sp,#0x150
0078b3d4  mov w1,#0x1c7
0078b3d8  ldp q29,q28,[sp, #0x110]
0078b3dc  mov w0,#0x10f
0078b3e0  mov w17,#0x168
0078b3e4  mov x16,x26
0078b3e8  ld1 {v8.2D,v9.2D,v10.2D,v11.2D},[x8]
0078b3ec  ldr w8,[sp, #0x2e8]
0078b3f0  ldr q30,[sp, #0x1a0]
0078b3f4  ldr q27,[sp, #0xf0]
0078b3f8  ldr q26,[sp, #0x130]
0078b3fc  sub w8,w8,#0x1
0078b400  cmp w8,#0x4
0078b404  b.hi 0x0078b368
0078b408  ldr x10,[sp, #0xd8]
0078b40c  adrp x13,0x3ee000
0078b410  add x13,x13,#0xbae
0078b414  ldr x11,[sp, #0x148]
0078b418  mul x9,x23,x16
0078b41c  madd x10,x11,x23,x10
0078b420  adr x11,0x78b434
0078b424  ldrh w12,[x13, x8, LSL #0x1]
0078b428  add x11,x11,x12, LSL #0x2
0078b42c  add x9,x19,x9, LSL #0x2
0078b430  br x11
0078bb58  ldr x0,[sp, #0x108]
0078bb5c  bl 0x00d16290
0078bb60  add x0,sp,#0x2a8
0078bb64  bl 0x00d20160
0078bb68  add x0,sp,#0x2a8
0078bb6c  bl 0x00d20170
0078bb70  ldr x0,[sp, #0xc8]
0078bb74  bl 0x00d15120
0078bb78  mov w0,#0x1
0078bb7c  ldr x19,[sp, #0xd0]
0078bb80  ldr x8,[x19, #0x28]
0078bb84  ldur x9,[x29, #-0x50]
0078bb88  cmp x8,x9
0078bb8c  b.ne 0x0078bc0c
0078bb90  add sp,sp,#0x530
0078bb94  ldp x20,x19,[sp, #0x90]
0078bb98  ldp x22,x21,[sp, #0x80]
0078bb9c  ldp x24,x23,[sp, #0x70]
0078bba0  ldp x26,x25,[sp, #0x60]
0078bba4  ldp x28,x27,[sp, #0x50]
0078bba8  ldp x29,x30,[sp, #0x40]
0078bbac  ldp d9,d8,[sp, #0x30]
0078bbb0  ldp d11,d10,[sp, #0x20]
0078bbb4  ldp d13,d12,[sp, #0x10]
0078bbb8  ldr d14,[sp], #0xa0
0078bbbc  ret
0078bbc0  adrp x8,0xd79000
0078bbc4  adrp x1,0x369000
0078bbc8  add x1,x1,#0xd05
0078bbcc  mov x2,x21
0078bbd0  ldr x8,[x8, #0xa18]
0078bbd4  ldr x0,[x8]
0078bbd8  bl 0x00d15110
0078bbdc  mov w0,wzr
0078bbe0  b 0x0078bb80
0078bc0c  bl 0x00d14d80

; ============================================================
; ilLoadTarga @ 00ad9f68
; body=[[00ad9f68, 00ada4e3] [00ada66c, 00ada75f]]
; ============================================================
00ad9f68  sub sp,sp,#0x180
00ad9f6c  stp x29,x30,[sp, #0x120]
00ad9f70  stp x28,x27,[sp, #0x130]
00ad9f74  stp x26,x25,[sp, #0x140]
00ad9f78  stp x24,x23,[sp, #0x150]
00ad9f7c  stp x22,x21,[sp, #0x160]
00ad9f80  stp x20,x19,[sp, #0x170]
00ad9f84  add x29,sp,#0x120
00ad9f88  mrs x24,tpidr_el0
00ad9f8c  ldr x8,[x24, #0x28]
00ad9f90  stur x8,[x29, #-0x10]
00ad9f94  bl 0x00d30f00
00ad9f98  cbz x0,0x00ada0d0
00ad9f9c  mov x19,x0
00ad9fa0  bl 0x00d30f50
00ad9fa4  bl 0x00d30f60
00ad9fa8  adrp x25,0xd7b000
00ad9fac  mov w20,w0
00ad9fb0  ldr x25,[x25, #0xd90]
00ad9fb4  ldr x8,[x25]
00ad9fb8  cbz x8,0x00ada0e0
00ad9fbc  add x0,sp,#0x10
00ad9fc0  mov w1,#0x12
00ad9fc4  mov w2,#0x1
00ad9fc8  stp xzr,xzr,[sp, #0x10]
00ad9fcc  strh wzr,[sp, #0x20]
00ad9fd0  bl 0x00d30fb0
00ad9fd4  mov w21,wzr
00ad9fd8  cmp w0,#0x1
00ad9fdc  b.ne 0x00ada0f4
00ad9fe0  ldrh w21,[sp, #0x1c]
00ad9fe4  cbz w21,0x00ada0e8
00ad9fe8  ldrh w22,[sp, #0x1e]
00ad9fec  cbz w22,0x00ada0e8
00ad9ff0  ldrb w8,[sp, #0x20]
00ad9ff4  cmp w8,#0x20
00ad9ff8  b.hi 0x00ada0e8
00ad9ffc  mov x10,#0x8100
00ada000  mov w9,#0x1
00ada004  movk x10,#0x101, LSL #16
00ada008  lsl x9,x9,x8
00ada00c  movk x10,#0x1, LSL #32
00ada010  tst x9,x10
00ada014  b.eq 0x00ada0e8
00ada018  ldrb w26,[sp, #0x21]
00ada01c  tbnz w26,#0x4,0x00ada0e8
00ada020  ldrb w27,[sp, #0x12]
00ada024  cmp w8,#0xf
00ada028  mov w9,#0x10
00ada02c  csel w28,w9,w8,eq
00ada030  cmp w27,#0xb
00ada034  b.hi 0x00ada248
00ada038  mov w8,#0x1
00ada03c  ldrb w23,[sp, #0x10]
00ada040  lsl w8,w8,w27
00ada044  mov w9,#0x202
00ada048  tst w8,w9
00ada04c  b.ne 0x00ada13c
00ada050  mov w9,#0x404
00ada054  tst w8,w9
00ada058  b.ne 0x00ada1c4
00ada05c  mov w8,#0x1
00ada060  mov w9,#0x808
00ada064  lsl w8,w8,w27
00ada068  tst w8,w9
00ada06c  b.eq 0x00ada248
00ada070  add x0,sp,#0x10
00ada074  mov w1,#0x1
00ada078  mov w2,w23
00ada07c  bl 0x00d30fb0
00ada080  cmp w0,w23
00ada084  b.ne 0x00ada4c0
00ada088  lsr w3,w28,#0x3
00ada08c  mov w0,w21
00ada090  mov w1,w22
00ada094  mov w2,#0x1
00ada098  mov w4,#0x1909
00ada09c  mov w5,#0x1401
00ada0a0  mov x6,xzr
00ada0a4  bl 0x00d254e0
00ada0a8  tst w0,#0xff
00ada0ac  b.eq 0x00ada4c0
00ada0b0  ldr x0,[x25]
00ada0b4  cmp w27,#0xb
00ada0b8  b.eq 0x00ada48c
00ada0bc  ldr x8,[x0, #0x18]
00ada0c0  mov w1,#0x1
00ada0c4  ldr w2,[x0, #0x20]
00ada0c8  mov x0,x8
00ada0cc  b 0x00ada4ac
00ada0d0  mov w0,#0x50a
00ada0d4  bl 0x00d30db0
00ada0d8  mov w21,wzr
00ada0dc  b 0x00ada108
00ada0e0  mov w0,#0x506
00ada0e4  b 0x00ada0ec
00ada0e8  mov w0,#0x508
00ada0ec  bl 0x00d30db0
00ada0f0  mov w21,wzr
00ada0f4  mov w0,w20
00ada0f8  mov w1,wzr
00ada0fc  bl 0x00d30f80
00ada100  mov x0,x19
00ada104  bl 0x00d30f10
00ada108  ldr x8,[x24, #0x28]
00ada10c  ldur x9,[x29, #-0x10]
00ada110  cmp x8,x9
00ada114  b.ne 0x00ada75c
00ada118  mov w0,w21
00ada11c  ldp x20,x19,[sp, #0x170]
00ada120  ldp x22,x21,[sp, #0x160]
00ada124  ldp x24,x23,[sp, #0x150]
00ada128  ldp x26,x25,[sp, #0x140]
00ada12c  ldp x28,x27,[sp, #0x130]
00ada130  ldp x29,x30,[sp, #0x120]
00ada134  add sp,sp,#0x180
00ada138  ret
00ada13c  ldrb w9,[sp, #0x15]
00ada140  add x0,sp,#0x10
00ada144  ldrb w8,[sp, #0x16]
00ada148  mov w1,#0x1
00ada14c  mov w2,w23
00ada150  stp w8,w9,[sp, #0x4]
00ada154  ldrb w8,[sp, #0x17]
00ada158  str w8,[sp, #0xc]
00ada15c  bl 0x00d30fb0
00ada160  cmp w0,w23
00ada164  b.ne 0x00ada4c0
00ada168  lsr w3,w28,#0x3
00ada16c  mov w0,w21
00ada170  mov w1,w22
00ada174  mov w2,#0x1
00ada178  mov w4,wzr
00ada17c  mov w5,#0x1401
00ada180  mov x6,xzr
00ada184  bl 0x00d254e0
00ada188  tst w0,#0xff
00ada18c  b.eq 0x00ada4c0
00ada190  ldp w9,w10,[sp, #0x4]
00ada194  ldr x8,[x25]
00ada198  lsl w9,w9,#0x8
00ada19c  ldr x0,[x8, #0x38]
00ada1a0  sxth w9,w9
00ada1a4  orr w21,w9,w10
00ada1a8  cbz x0,0x00ada258
00ada1ac  ldr w9,[x8, #0x40]
00ada1b0  ldr w22,[sp, #0xc]
00ada1b4  cbz w9,0x00ada25c
00ada1b8  bl 0x00d30dc0
00ada1bc  ldr x8,[x25]
00ada1c0  b 0x00ada25c
00ada1c4  add x0,sp,#0x10
00ada1c8  mov w1,#0x1
00ada1cc  mov w2,w23
00ada1d0  bl 0x00d30fb0
00ada1d4  cmp w0,w23
00ada1d8  b.ne 0x00ada4c0
00ada1dc  lsr w3,w28,#0x3
00ada1e0  mov w0,w21
00ada1e4  mov w1,w22
00ada1e8  mov w2,#0x1
00ada1ec  mov w4,wzr
00ada1f0  mov w5,#0x1401
00ada1f4  mov x6,xzr
00ada1f8  bl 0x00d254e0
00ada1fc  tst w0,#0xff
00ada200  b.eq 0x00ada4c0
00ada204  ldr x0,[x25]
00ada208  ldrb w8,[x0, #0xc]
00ada20c  sub w8,w8,#0x1
00ada210  and w9,w8,#0xff
00ada214  cmp w9,#0x4
00ada218  b.cs 0x00ada250
00ada21c  sxtb x8,w8
00ada220  adrp x9,0x3b1000
00ada224  add x9,x9,#0x5b0
00ada228  cmp w27,#0xa
00ada22c  ldr w8,[x9, x8, LSL #0x2]
00ada230  str w8,[x0, #0x28]
00ada234  b.ne 0x00ada298
00ada238  bl 0x00adaf30
00ada23c  tst w0,#0xff
00ada240  b.ne 0x00ada2bc
00ada244  b 0x00ada4c0
00ada248  mov w0,#0x507
00ada24c  b 0x00ada0ec
00ada250  mov w0,#0x505
00ada254  b 0x00ada45c
00ada258  ldr w22,[sp, #0xc]
00ada25c  lsr w9,w22,#0x3
00ada260  mov w10,#0x1900
00ada264  cmp w22,#0x20
00ada268  mul w0,w21,w9
00ada26c  str w10,[x8, #0x28]
00ada270  str w0,[x8, #0x40]
00ada274  b.eq 0x00ada39c
00ada278  cmp w22,#0x18
00ada27c  b.eq 0x00ada3a4
00ada280  cmp w22,#0x10
00ada284  b.ne 0x00ada458
00ada288  mov w9,#0x406
00ada28c  lsl w0,w21,#0x2
00ada290  stp w0,w9,[x8, #0x40]
00ada294  b 0x00ada3ac
00ada298  ldr x8,[x0, #0x18]
00ada29c  mov w1,#0x1
00ada2a0  ldr w2,[x0, #0x20]
00ada2a4  mov x0,x8
00ada2a8  bl 0x00d30fb0
00ada2ac  ldr x8,[x25]
00ada2b0  ldr w8,[x8, #0x20]
00ada2b4  cmp w0,w8
00ada2b8  b.ne 0x00ada4c0
00ada2bc  cmp w28,#0x10
00ada2c0  b.ne 0x00ada498
00ada2c4  ldr x22,[x25]
00ada2c8  ldp w8,w9,[x22]
00ada2cc  mul w23,w9,w8
00ada2d0  add w0,w23,w23, LSL #0x1
00ada2d4  bl 0x00d30da0
00ada2d8  mov x21,x0
00ada2dc  cbz x0,0x00ada4c4
00ada2e0  cbz w23,0x00ada368
00ada2e4  ldr x9,[x22, #0x18]
00ada2e8  cmp w23,#0x8
00ada2ec  b.cc 0x00ada31c
00ada2f0  sub w8,w23,#0x1
00ada2f4  ubfiz x10,x8,#0x1,#0x20
00ada2f8  add x11,x10,x9
00ada2fc  add x11,x11,#0x2
00ada300  cmp x21,x11
00ada304  b.cs 0x00ada66c
00ada308  add x10,x10,x8
00ada30c  add x10,x10,x21
00ada310  add x10,x10,#0x3
00ada314  cmp x9,x10
00ada318  b.cs 0x00ada66c
00ada31c  mov w13,wzr
00ada320  mov x10,x9
00ada324  mov x11,x21
00ada328  sub w8,w23,w13
00ada32c  ldrb w9,[x10]
00ada330  subs w8,w8,#0x1
00ada334  ldrb w12,[x10, #0x1]
00ada338  add x10,x10,#0x2
00ada33c  orr w13,w9,w12, LSL #0x8
00ada340  lsl w12,w12,#0x1
00ada344  lsr w13,w13,#0x2
00ada348  lsl w9,w9,#0x3
00ada34c  and w12,w12,#0xf8
00ada350  and w13,w13,#0xf8
00ada354  strb w9,[x11]
00ada358  strb w12,[x11, #0x2]
00ada35c  strb w13,[x11, #0x1]
00ada360  add x11,x11,#0x3
00ada364  b.ne 0x00ada32c
00ada368  ldp w0,w1,[x22]
00ada36c  mov w2,#0x1
00ada370  mov w3,#0x3
00ada374  mov w4,#0x80e0
00ada378  mov w5,#0x1401
00ada37c  mov x6,x21
00ada380  bl 0x00d254e0
00ada384  mov w22,w0
00ada388  mov x0,x21
00ada38c  bl 0x00d30dc0
00ada390  tst w22,#0xff
00ada394  cset w21,ne
00ada398  b 0x00ada4c4
00ada39c  mov w9,#0x406
00ada3a0  b 0x00ada3a8
00ada3a4  mov w9,#0x404
00ada3a8  str w9,[x8, #0x44]
00ada3ac  bl 0x00d30da0
00ada3b0  ldr x8,[x25]
00ada3b4  str x0,[x8, #0x38]
00ada3b8  cbz x0,0x00ada4c0
00ada3bc  ldr w2,[x8, #0x40]
00ada3c0  cmp w22,#0x10
00ada3c4  b.ne 0x00ada468
00ada3c8  mov w1,wzr
00ada3cc  bl 0x00d15920
00ada3d0  ldr x8,[x25]
00ada3d4  ldr w9,[x8, #0x40]
00ada3d8  cbz w9,0x00ada480
00ada3dc  mov w22,wzr
00ada3e0  bl 0x00d30ff0
00ada3e4  mov w21,w0
00ada3e8  bl 0x00d30f90
00ada3ec  tst w0,#0xff
00ada3f0  b.ne 0x00ada4c0
00ada3f4  ldr x8,[x25]
00ada3f8  lsr w9,w21,#0xc
00ada3fc  and w9,w9,#0x8
00ada400  add w22,w22,#0x4
00ada404  ldr x8,[x8, #0x38]
00ada408  strb w9,[x8, #0x3]
00ada40c  lsr w9,w21,#0x7
00ada410  ldr x8,[x25]
00ada414  and w9,w9,#0xf8
00ada418  ldr x8,[x8, #0x38]
00ada41c  strb w9,[x8]
00ada420  lsr w9,w21,#0x2
00ada424  ldr x8,[x25]
00ada428  and w9,w9,#0xf8
00ada42c  ldr x8,[x8, #0x38]
00ada430  strb w9,[x8, #0x1]
00ada434  lsl w9,w21,#0x3
00ada438  ldr x8,[x25]
00ada43c  ldr x8,[x8, #0x38]
00ada440  strb w9,[x8, #0x2]
00ada444  ldr x8,[x25]
00ada448  ldr w9,[x8, #0x40]
00ada44c  cmp w22,w9
00ada450  b.cc 0x00ada3e0
00ada454  b 0x00ada480
00ada458  mov w0,#0x507
00ada45c  bl 0x00d30db0
00ada460  mov w21,wzr
00ada464  b 0x00ada4c4
00ada468  mov w1,#0x1
00ada46c  bl 0x00d30fb0
00ada470  ldr x8,[x25]
00ada474  ldr w9,[x8, #0x40]
00ada478  cmp w0,w9
00ada47c  b.ne 0x00ada4c0
00ada480  cmp w27,#0x9
00ada484  b.ne 0x00ada4a0
00ada488  mov x0,x8
00ada48c  bl 0x00adaf30
00ada490  tst w0,#0xff
00ada494  b.eq 0x00ada4c0
00ada498  mov w21,#0x1
00ada49c  b 0x00ada4c4
00ada4a0  ldr x0,[x8, #0x18]
00ada4a4  mov w1,#0x1
00ada4a8  ldr w2,[x8, #0x20]
00ada4ac  bl 0x00d30fb0
00ada4b0  ldr x8,[x25]
00ada4b4  ldr w8,[x8, #0x20]
00ada4b8  cmp w0,w8
00ada4bc  b.eq 0x00ada498
00ada4c0  mov w21,wzr
00ada4c4  ubfx w9,w26,#0x4,#0x2
00ada4c8  adrp x10,0x54b000
00ada4cc  add x10,x10,#0x328
00ada4d0  mov w8,#0x601
00ada4d4  adr x11,0xada4e4
00ada4d8  ldrb w12,[x10, x9]
00ada4dc  add x11,x11,x12, LSL #0x2
00ada4e0  br x11
00ada66c  add x8,x8,#0x1
00ada670  cmp w23,#0x10
00ada674  b.cs 0x00ada6e4
00ada678  mov x12,xzr
00ada67c  and x13,x8,#0x1fffffff8
00ada680  lsl x15,x12,#0x1
00ada684  lsl x11,x13,#0x1
00ada688  add x14,x15,x12
00ada68c  add x10,x9,x11
00ada690  add x11,x11,x13
00ada694  movi v0.8B,#0xf8
00ada698  add x14,x21,x14
00ada69c  add x11,x21,x11
00ada6a0  add x9,x9,x15
00ada6a4  sub x12,x12,x13
00ada6a8  ld2 {v1.8B,v2.8B},[x9], #0x10
00ada6ac  uxtl v3.8H,v1.8B
00ada6b0  adds x12,x12,#0x8
00ada6b4  shll v4.8H,v2.8B,#0x8
00ada6b8  orr v3.16B,v4.16B,v3.16B
00ada6bc  shl v4.8B,v1.8B,0x3
00ada6c0  shrn v3.8B,v3.8H,#0x2
00ada6c4  shl v1.8B,v2.8B,0x1
00ada6c8  and v5.8B,v3.8B,v0.8B
00ada6cc  and v6.8B,v1.8B,v0.8B
00ada6d0  st3 {v4.8B,v5.8B,v6.8B},[x14], #0x18
00ada6d4  b.ne 0x00ada6a8
00ada6d8  cmp x8,x13
00ada6dc  b.ne 0x00ada328
00ada6e0  b 0x00ada368
00ada6e4  and x12,x8,#0x1fffffff0
00ada6e8  mov x11,x9
00ada6ec  movi v0.16B,#0xf8
00ada6f0  mov x10,x12
00ada6f4  mov x13,x21
00ada6f8  ld2 {v1.16B,v2.16B},[x11], #0x20
00ada6fc  uxtl v3.8H,v1.8B
00ada700  subs x10,x10,#0x10
00ada704  shll v5.8H,v2.8B,#0x8
00ada708  uxtl2 v4.8H,v1.16B
00ada70c  shll2 v6.8H,v2.16B,#0x8
00ada710  orr v3.16B,v5.16B,v3.16B
00ada714  shrn v3.8B,v3.8H,#0x2
00ada718  orr v4.16B,v6.16B,v4.16B
00ada71c  shrn2 v3.16B,v4.8H,#0x2
00ada720  shl v4.16B,v1.16B,0x3
00ada724  shl v1.16B,v2.16B,0x1
00ada728  and v5.16B,v3.16B,v0.16B
00ada72c  and v6.16B,v1.16B,v0.16B
00ada730  st3 {v4.16B,v5.16B,v6.16B},[x13], #0x30
00ada734  b.ne 0x00ada6f8
00ada738  cmp x8,x12
00ada73c  b.eq 0x00ada368
00ada740  tbnz w8,#0x3,0x00ada67c
00ada744  lsl x8,x12,#0x1
00ada748  mov w13,w12
00ada74c  add x10,x8,x12
00ada750  add x11,x21,x10
00ada754  add x10,x9,x8
00ada758  b 0x00ada328
00ada75c  bl 0x00d14d80

; ============================================================
; FUN_00bb7394 @ 00bb7394
; body=[[00bb7394, 00bb7657] [00bb76b8, 00bb76d7] [00bb7ae0, 00bb7ba7] [00bb8284, 00bb82ff]]
; ============================================================
00bb7394  sub sp,sp,#0x190
00bb7398  stp x29,x30,[sp, #0x130]
00bb739c  stp x28,x27,[sp, #0x140]
00bb73a0  stp x26,x25,[sp, #0x150]
00bb73a4  stp x24,x23,[sp, #0x160]
00bb73a8  stp x22,x21,[sp, #0x170]
00bb73ac  stp x20,x19,[sp, #0x180]
00bb73b0  add x29,sp,#0x130
00bb73b4  mov x19,x0
00bb73b8  cmp w2,w1
00bb73bc  b.ne 0x00bb73c8
00bb73c0  mov x23,x19
00bb73c4  b 0x00bb82a8
00bb73c8  mov w20,w3
00bb73cc  mov w21,w2
00bb73d0  orr w8,w3,w2
00bb73d4  tbnz w8,#0x1f,0x00bb8284
00bb73d8  mov w24,w4
00bb73dc  mov w22,w1
00bb73e0  cbz w20,0x00bb73f4
00bb73e4  mov w8,#0x7fffffff
00bb73e8  udiv w8,w8,w20
00bb73ec  cmp w8,w21
00bb73f0  b.lt 0x00bb8284
00bb73f4  mul w25,w20,w21
00bb73f8  orr w8,w25,w24
00bb73fc  tbnz w8,#0x1f,0x00bb8284
00bb7400  cbz w24,0x00bb7414
00bb7404  mov w8,#0x7fffffff
00bb7408  udiv w8,w8,w24
00bb740c  cmp w8,w25
00bb7410  b.lt 0x00bb8284
00bb7414  mul w8,w25,w24
00bb7418  sxtw x0,w8
00bb741c  bl 0x00d16320
00bb7420  cbz x0,0x00bb8284
00bb7424  mov x23,x0
00bb7428  cmp w24,#0x1
00bb742c  b.lt 0x00bb82cc
00bb7430  add w13,w21,w22, LSL #0x3
00bb7434  cmp w13,#0x23
00bb7438  b.hi 0x00bb82d8
00bb743c  mov x9,#0x1c00
00bb7440  mov w8,#0x1
00bb7444  movk x9,#0x161a, LSL #16
00bb7448  lsl x8,x8,x13
00bb744c  movk x9,#0xe, LSL #32
00bb7450  tst x8,x9
00bb7454  b.eq 0x00bb82d8
00bb7458  sub w9,w20,#0x1
00bb745c  mov w16,#0x10
00bb7460  add x10,x9,#0x1
00bb7464  mov w12,w24
00bb7468  and x17,x10,#0x1fffffff0
00bb746c  and x1,x10,#0x1fffffff8
00bb7470  lsl x15,x17,#0x2
00bb7474  lsl x0,x17,#0x1
00bb7478  lsl x2,x1,#0x1
00bb747c  stur x10,[x29, #-0x18]
00bb7480  stur x17,[x29, #-0x40]
00bb7484  movi v4.8B,#0x4d
00bb7488  str x15,[sp]
00bb748c  sub w15,w9,w17
00bb7490  movi v1.2D,#-0x1
00bb7494  movi v5.8B,#0x96
00bb7498  movi v3.2D,#-0x1
00bb749c  mul w24,w20,w22
00bb74a0  str w15,[sp, #0x48]
00bb74a4  sub w15,w9,w1
00bb74a8  movi v6.8B,#0x1d
00bb74ac  mov w14,wzr
00bb74b0  movi v7.16B,#0x4d
00bb74b4  mov w11,wzr
00bb74b8  stur w15,[x29, #-0x2c]
00bb74bc  ands x15,x10,#0xf
00bb74c0  csel x15,x16,x15,eq
00bb74c4  lsl x16,x1,#0x2
00bb74c8  sub x3,x10,x15
00bb74cc  mov x8,xzr
00bb74d0  lsl x4,x3,#0x2
00bb74d4  stur x12,[x29, #-0x10]
00bb74d8  stur x16,[x29, #-0x60]
00bb74dc  mov w16,#0x8
00bb74e0  str x15,[sp, #0x78]
00bb74e4  ands x15,x10,#0x7
00bb74e8  csel x15,x16,x15,eq
00bb74ec  sub w16,w9,w3
00bb74f0  str x3,[sp, #0x90]
00bb74f4  sub x3,x10,x15
00bb74f8  movi v16.16B,#0x96
00bb74fc  sub w13,w13,#0xa
00bb7500  str w16,[sp, #0x34]
00bb7504  sub w16,w9,w3
00bb7508  movi v17.16B,#0x1d
00bb750c  stur x1,[x29, #-0x20]
00bb7510  add x28,x19,#0x10
00bb7514  mov w26,#0x4d
00bb7518  stur w16,[x29, #-0x4c]
00bb751c  lsl x16,x3,#0x2
00bb7520  mov w30,#0x96
00bb7524  mov w7,#0x1d
00bb7528  adrp x12,0x55e000
00bb752c  add x12,x12,#0xc49
00bb7530  stur x16,[x29, #-0x88]
00bb7534  add x16,x0,x17
00bb7538  mov w17,#0x20
00bb753c  str x4,[sp, #0x38]
00bb7540  stp x16,x0,[sp, #0x18]
00bb7544  add x16,x2,x1
00bb7548  and x0,x10,#0x1ffffffe0
00bb754c  stp x16,x2,[x29, #-0x70]
00bb7550  lsl x16,x0,#0x1
00bb7554  mov w2,#0xff
00bb7558  stur x0,[x29, #-0x28]
00bb755c  str x16,[sp, #0x10]
00bb7560  add x16,x16,x0
00bb7564  str x16,[sp, #0x8]
00bb7568  lsl x16,x0,#0x2
00bb756c  str x16,[sp, #0x40]
00bb7570  ands x16,x10,#0x1f
00bb7574  csel x17,x17,x16,eq
00bb7578  mvn x16,x9
00bb757c  add x15,x16,x15
00bb7580  sub w16,w9,w0
00bb7584  str x17,[sp, #0x98]
00bb7588  stur x15,[x29, #-0x58]
00bb758c  sub x15,x10,x17
00bb7590  and x10,x10,#0x18
00bb7594  str w16,[sp, #0x4c]
00bb7598  lsl x16,x15,#0x1
00bb759c  stur x15,[x29, #-0x48]
00bb75a0  str x10,[sp, #0x88]
00bb75a4  add x10,x16,x15
00bb75a8  stp x10,x16,[sp, #0x68]
00bb75ac  sub w10,w9,w15
00bb75b0  add x16,x19,#0x20
00bb75b4  str w10,[sp, #0x84]
00bb75b8  lsl x10,x3,#0x1
00bb75bc  stp x10,x3,[x29, #-0x80]
00bb75c0  add x10,x10,x3
00bb75c4  stur x10,[x29, #-0x90]
00bb75c8  lsl x10,x15,#0x2
00bb75cc  str x10,[sp, #0x28]
00bb75d0  neg x10,x1
00bb75d4  add x1,x23,#0x40
00bb75d8  stur x10,[x29, #-0x38]
00bb75dc  add x10,x23,#0x10
00bb75e0  str x10,[sp, #0x60]
00bb75e4  add x10,x23,#0x20
00bb75e8  str x10,[sp, #0x58]
00bb75ec  add x10,x19,#0x40
00bb75f0  str x10,[sp, #0x50]
00bb75f4  b 0x00bb7610
00bb75f8  ldur x10,[x29, #-0x10]
00bb75fc  add x8,x8,#0x1
00bb7600  add w11,w0,w24
00bb7604  add w14,w3,w25
00bb7608  cmp x8,x10
00bb760c  b.eq 0x00bb82cc
00bb7610  mul w15,w8,w20
00bb7614  mov w3,w14
00bb7618  mov w0,w11
00bb761c  add x6,x23,x3
00bb7620  cmp w13,#0x18
00bb7624  mul w17,w15,w22
00bb7628  mul w14,w15,w21
00bb762c  add x17,x19,x17
00bb7630  add x14,x23,x14
00bb7634  b.hi 0x00bb76b8
00bb7638  adr x4,0xbb7658
00bb763c  ldrb w10,[x12, x13]
00bb7640  add x4,x4,x10, LSL #0x2
00bb7644  add x15,x28,x0
00bb7648  add x11,x1,x3
00bb764c  add x27,x16,x0
00bb7650  add x5,x19,x0
00bb7654  br x4
00bb76b8  tbnz w9,#0x1f,0x00bb75f8
00bb76bc  mov w11,w9
00bb76c0  cmp w9,#0x8
00bb76c4  b.cc 0x00bb7b7c
00bb76c8  cmp w9,#0x20
00bb76cc  b.cs 0x00bb7ae0
00bb76d0  mov x5,xzr
00bb76d4  b 0x00bb7b3c
00bb7ae0  ldr x10,[sp, #0x50]
00bb7ae4  ldur x15,[x29, #-0x48]
00bb7ae8  add x11,x10,x0
00bb7aec  sub x10,x11,#0x40
00bb7af0  ld4 {v22.16B,v23.16B,v24.16B,v25.16B},[x11]
00bb7af4  add x11,x11,#0x80
00bb7af8  subs x15,x15,#0x20
00bb7afc  ld4 {v18.16B,v19.16B,v20.16B,v21.16B},[x10]
00bb7b00  add x10,x6,#0x60
00bb7b04  st3 {v18.16B,v19.16B,v20.16B},[x6], #0x30
00bb7b08  st3 {v22.16B,v23.16B,v24.16B},[x6]
00bb7b0c  mov x6,x10
00bb7b10  b.ne 0x00bb7aec
00bb7b14  ldr x10,[sp, #0x98]
00bb7b18  ldur x5,[x29, #-0x48]
00bb7b1c  cmp x10,#0x8
00bb7b20  b.hi 0x00bb7b3c
00bb7b24  ldr x10,[sp, #0x28]
00bb7b28  ldr w11,[sp, #0x84]
00bb7b2c  add x17,x17,x10
00bb7b30  ldr x10,[sp, #0x68]
00bb7b34  add x14,x14,x10
00bb7b38  b 0x00bb7b7c
00bb7b3c  ldur x10,[x29, #-0x90]
00bb7b40  add x15,x5,x5, LSL #0x1
00bb7b44  add x14,x14,x10
00bb7b48  ldur x10,[x29, #-0x88]
00bb7b4c  add x17,x17,x10
00bb7b50  add x10,x0,x5, LSL #0x2
00bb7b54  add x11,x19,x10
00bb7b58  add x10,x15,x3
00bb7b5c  add x15,x23,x10
00bb7b60  ldur x10,[x29, #-0x58]
00bb7b64  add x5,x10,x5
00bb7b68  ld4 {v18.8B,v19.8B,v20.8B,v21.8B},[x11], #0x20
00bb7b6c  st3 {v18.8B,v19.8B,v20.8B},[x15], #0x18
00bb7b70  adds x5,x5,#0x8
00bb7b74  b.ne 0x00bb7b68
00bb7b78  ldur w11,[x29, #-0x4c]
00bb7b7c  add w11,w11,#0x1
00bb7b80  ldrb w10,[x17]
00bb7b84  sub w11,w11,#0x1
00bb7b88  ldurh w15,[x17, #0x1]
00bb7b8c  add x17,x17,#0x4
00bb7b90  cmp w11,#0x0
00bb7b94  strb w10,[x14]
00bb7b98  sturh w15,[x14, #0x1]
00bb7b9c  add x14,x14,#0x3
00bb7ba0  b.gt 0x00bb7b80
00bb7ba4  b 0x00bb75f8
00bb8284  mov x0,x19
00bb8288  bl 0x00d16290
00bb828c  adrp x0,0xe06000
00bb8290  add x0,x0,#0xfe0
00bb8294  bl 0x00d1bb10
00bb8298  adrp x8,0x38a000
00bb829c  add x8,x8,#0x567
00bb82a0  mov x23,xzr
00bb82a4  str x8,[x0]
00bb82a8  mov x0,x23
00bb82ac  ldp x20,x19,[sp, #0x180]
00bb82b0  ldp x22,x21,[sp, #0x170]
00bb82b4  ldp x24,x23,[sp, #0x160]
00bb82b8  ldp x26,x25,[sp, #0x150]
00bb82bc  ldp x28,x27,[sp, #0x140]
00bb82c0  ldp x29,x30,[sp, #0x130]
00bb82c4  add sp,sp,#0x190
00bb82c8  ret
00bb82cc  mov x0,x19
00bb82d0  bl 0x00d16290
00bb82d4  b 0x00bb82a8
00bb82d8  mov x0,x19
00bb82dc  bl 0x00d16290
00bb82e0  mov x0,x23
00bb82e4  bl 0x00d16290
00bb82e8  adrp x0,0xe06000
00bb82ec  add x0,x0,#0xfe0
00bb82f0  bl 0x00d1bb10
00bb82f4  adrp x8,0x3a6000
00bb82f8  add x8,x8,#0x1db
00bb82fc  b 0x00bb82a0

; ============================================================
; FUN_00bf8cd4 @ 00bf8cd4
; body=[[00bf8cd4, 00bf8eb7]]
; ============================================================
00bf8cd4  sub sp,sp,#0x90
00bf8cd8  stp x29,x30,[sp, #0x30]
00bf8cdc  stp x28,x27,[sp, #0x40]
00bf8ce0  stp x26,x25,[sp, #0x50]
00bf8ce4  stp x24,x23,[sp, #0x60]
00bf8ce8  stp x22,x21,[sp, #0x70]
00bf8cec  stp x20,x19,[sp, #0x80]
00bf8cf0  add x29,sp,#0x30
00bf8cf4  sub w9,w4,#0x1
00bf8cf8  lsr w19,w2,#0x1
00bf8cfc  lsr w28,w4,#0x1
00bf8d00  mov w20,w5
00bf8d04  sub w8,w19,w28
00bf8d08  mov w23,w4
00bf8d0c  mov x21,x1
00bf8d10  mov x22,x0
00bf8d14  mov x27,xzr
00bf8d18  stur x9,[x29, #-0x10]
00bf8d1c  sxtw x9,w8
00bf8d20  mov w25,w2
00bf8d24  ubfiz x8,x28,#0x1,#0x20
00bf8d28  and x26,x28,#0x3ffffff0
00bf8d2c  and x24,x28,#0x3ffffff8
00bf8d30  str w3,[sp, #0x4]
00bf8d34  str x0,[sp, #0x8]
00bf8d38  stp x8,x9,[sp, #0x10]
00bf8d3c  stur x1,[x29, #-0x8]
00bf8d40  b 0x00bf8d58
00bf8d44  add x27,x27,#0x1
00bf8d48  add x21,x21,x25
00bf8d4c  add x22,x22,x19
00bf8d50  cmp w27,w20
00bf8d54  b.eq 0x00bf8e64
00bf8d58  cmp w23,#0x10
00bf8d5c  b.cc 0x00bf8d94
00bf8d60  ldr x8,[sp, #0x10]
00bf8d64  ldur x9,[x29, #-0x8]
00bf8d68  nop
00bf8d6c  madd x8,x27,x25,x8
00bf8d70  add x8,x9,x8
00bf8d74  cmp x22,x8
00bf8d78  b.cs 0x00bf8de4
00bf8d7c  ldr x9,[sp, #0x8]
00bf8d80  nop
00bf8d84  madd x8,x27,x19,x28
00bf8d88  add x8,x9,x8
00bf8d8c  cmp x21,x8
00bf8d90  b.cs 0x00bf8de4
00bf8d94  mov x8,xzr
00bf8d98  lsl x9,x8,#0x1
00bf8d9c  add x10,x21,x9
00bf8da0  add x9,x9,#0x2
00bf8da4  ldrb w11,[x10]
00bf8da8  ldrb w10,[x10, #0x1]
00bf8dac  orr w10,w11,w10, LSL #0x4
00bf8db0  strb w10,[x22, x8]
00bf8db4  add x8,x8,#0x1
00bf8db8  cmp x28,x8
00bf8dbc  b.ne 0x00bf8d9c
00bf8dc0  cmp w19,w28
00bf8dc4  b.ls 0x00bf8d44
00bf8dc8  ldur x8,[x29, #-0x10]
00bf8dcc  add x0,x22,x28
00bf8dd0  ldr x2,[sp, #0x18]
00bf8dd4  ldrb w8,[x21, x8]
00bf8dd8  add w1,w8,w8, LSL #0x4
00bf8ddc  bl 0x00d15920
00bf8de0  b 0x00bf8d44
00bf8de4  cmp w23,#0x20
00bf8de8  b.cs 0x00bf8df4
00bf8dec  mov x9,xzr
00bf8df0  b 0x00bf8e2c
00bf8df4  mov x8,xzr
00bf8df8  mov x9,x21
00bf8dfc  ld2 {v0.16B,v1.16B},[x9], #0x20
00bf8e00  shl v2.16B,v1.16B,0x4
00bf8e04  orr v0.16B,v2.16B,v0.16B
00bf8e08  str q0,[x22,x8]
00bf8e0c  add x8,x8,#0x10
00bf8e10  cmp x26,x8
00bf8e14  b.ne 0x00bf8dfc
00bf8e18  cmp x26,x28
00bf8e1c  b.eq 0x00bf8dc0
00bf8e20  mov x9,x26
00bf8e24  mov x8,x26
00bf8e28  tbz w28,#0x3,0x00bf8d98
00bf8e2c  lsl x8,x9,#0x1
00bf8e30  add x10,x21,x8
00bf8e34  add x8,x8,#0x10
00bf8e38  ld2 {v0.8B,v1.8B},[x10]
00bf8e3c  shl v2.8B,v1.8B,0x4
00bf8e40  orr v0.8B,v2.8B,v0.8B
00bf8e44  str d0,[x22,x9]
00bf8e48  add x9,x9,#0x8
00bf8e4c  cmp x24,x9
00bf8e50  b.ne 0x00bf8e30
00bf8e54  mov x8,x24
00bf8e58  cmp x24,x28
00bf8e5c  b.eq 0x00bf8dc0
00bf8e60  b 0x00bf8d98
00bf8e64  ldr w9,[sp, #0x4]
00bf8e68  cmp w20,w9
00bf8e6c  b.ge 0x00bf8e98
00bf8e70  neg w8,w19
00bf8e74  sub w20,w9,w20
00bf8e78  add x23,x22,w8, SXTW 
00bf8e7c  mov x0,x22
00bf8e80  mov x1,x23
00bf8e84  mov x2,x19
00bf8e88  bl 0x00d159f0
00bf8e8c  add x22,x22,x19
00bf8e90  subs w20,w20,#0x1
00bf8e94  b.ne 0x00bf8e7c
00bf8e98  ldp x20,x19,[sp, #0x80]
00bf8e9c  ldp x22,x21,[sp, #0x70]
00bf8ea0  ldp x24,x23,[sp, #0x60]
00bf8ea4  ldp x26,x25,[sp, #0x50]
00bf8ea8  ldp x28,x27,[sp, #0x40]
00bf8eac  ldp x29,x30,[sp, #0x30]
00bf8eb0  add sp,sp,#0x90
00bf8eb4  ret

; ============================================================
; FUN_00c9bce4 @ 00c9bce4
; body=[[00c9bce4, 00c9c7df]]
; ============================================================
00c9bce4  bti c
00c9bce8  sub sp,sp,#0x90
00c9bcec  stp d15,d14,[sp, #0x50]
00c9bcf0  stp d13,d12,[sp, #0x60]
00c9bcf4  stp d11,d10,[sp, #0x70]
00c9bcf8  stp d9,d8,[sp, #0x80]
00c9bcfc  ldr d0,[x0]
00c9bd00  ldur d1,[x1, #-0x8]
00c9bd04  fcmp d0,d1
00c9bd08  b.pl 0x00c9bd20
00c9bd0c  mov x9,x0
00c9bd10  ldr d1,[x9, #0x8]!
00c9bd14  fcmp d0,d1
00c9bd18  b.pl 0x00c9bd10
00c9bd1c  b 0x00c9bd40
00c9bd20  add x8,x0,#0x8
00c9bd24  mov x9,x8
00c9bd28  cmp x8,x1
00c9bd2c  b.cs 0x00c9bd40
00c9bd30  mov x8,x9
00c9bd34  ldr d1,[x8], #0x8
00c9bd38  fcmp d0,d1
00c9bd3c  b.pl 0x00c9bd24
00c9bd40  cmp x9,x1
00c9bd44  b.cs 0x00c9bd54
00c9bd48  ldr d1,[x1, #-0x8]!
00c9bd4c  fcmp d0,d1
00c9bd50  b.mi 0x00c9bd48
00c9bd54  mov x10,x9
00c9bd58  cmp x9,x1
00c9bd5c  b.cs 0x00c9bd74
00c9bd60  ldr d1,[x1]
00c9bd64  mov x10,x9
00c9bd68  ldr d2,[x9]
00c9bd6c  str d1,[x10], #0x8
00c9bd70  str d2,[x1]
00c9bd74  sub x8,x1,#0x8
00c9bd78  sub x2,x8,x10
00c9bd7c  cmp x2,#0x3f1
00c9bd80  b.lt 0x00c9c4ac
00c9bd84  adrp x13,0x3b0000
00c9bd88  adrp x15,0x3b2000
00c9bd8c  adrp x14,0x3b2000
00c9bd90  adrp x16,0x3b1000
00c9bd94  mov x12,xzr
00c9bd98  mov x11,xzr
00c9bd9c  ldr q5,[x13, #0xae0]
00c9bda0  adrp x13,0x3b0000
00c9bda4  ldr q7,[x15, #0x510]
00c9bda8  adrp x15,0x3b1000
00c9bdac  ldr q6,[x14, #0x1b0]
00c9bdb0  adrp x14,0x3b1000
00c9bdb4  ldr q17,[x13, #0xbb0]
00c9bdb8  adrp x13,0x3b0000
00c9bdbc  ldr q19,[x15, #0x250]
00c9bdc0  adrp x15,0x3b1000
00c9bdc4  ldr q18,[x14, #0x460]
00c9bdc8  adrp x14,0x3b1000
00c9bdcc  ldr q20,[x13, #0xf80]
00c9bdd0  adrp x13,0x3b0000
00c9bdd4  ldr q22,[x15, #0x360]
00c9bdd8  adrp x15,0x3b1000
00c9bddc  ldr q21,[x14, #0x470]
00c9bde0  adrp x14,0x3b0000
00c9bde4  ldr q23,[x13, #0x8f0]
00c9bde8  adrp x13,0x3b1000
00c9bdec  ldr q25,[x15, #0x9b0]
00c9bdf0  adrp x15,0x3b1000
00c9bdf4  ldr q24,[x14, #0xaf0]
00c9bdf8  adrp x14,0x3b0000
00c9bdfc  ldr q26,[x13, #0xbc0]
00c9be00  adrp x13,0x3b2000
00c9be04  ldr q28,[x15, #0xf40]
00c9be08  adrp x15,0x3b0000
00c9be0c  ldr q27,[x14, #0xa00]
00c9be10  adrp x14,0x3b1000
00c9be14  ldr q29,[x13, #0x80]
00c9be18  adrp x13,0x3b2000
00c9be1c  ldr q31,[x15, #0xfa0]
00c9be20  adrp x15,0x3b1000
00c9be24  ldr q30,[x14, #0x5f0]
00c9be28  adrp x14,0x3b0000
00c9be2c  ldr q8,[x13, #0x530]
00c9be30  adrp x13,0x3b0000
00c9be34  ldr q10,[x15, #0x530]
00c9be38  adrp x15,0x3b0000
00c9be3c  ldr q9,[x14, #0xbc0]
00c9be40  adrp x14,0x3b1000
00c9be44  ldr q11,[x13, #0xf90]
00c9be48  adrp x13,0x3b2000
00c9be4c  ldr q1,[x15, #0x7d0]
00c9be50  adrp x15,0x3b1000
00c9be54  ldr q12,[x14, #0xbd0]
00c9be58  adrp x14,0x3b2000
00c9be5c  ldr q16,[x16, #0x840]
00c9be60  adrp x16,0x3b1000
00c9be64  str q1,[sp, #0x40]
00c9be68  ldr q1,[x13, #0x420]
00c9be6c  adrp x13,0x3b1000
00c9be70  mov x17,#-0x200
00c9be74  dup v13.2D,v0.D[0x0]
00c9be78  str q1,[sp, #0x30]
00c9be7c  ldr q1,[x14, #0x90]
00c9be80  adrp x14,0x3b1000
00c9be84  str q1,[sp, #0x20]
00c9be88  ldr q1,[x15, #0x370]
00c9be8c  adrp x15,0x3b0000
00c9be90  stp q0,q1,[sp]
00c9be94  b 0x00c9bebc
00c9be98  cmp x11,#0x0
00c9be9c  cset w2,eq
00c9bea0  cmp x12,#0x0
00c9bea4  csel x3,x17,xzr,eq
00c9bea8  add x10,x10,x2, LSL #0x9
00c9beac  add x8,x8,x3
00c9beb0  sub x2,x8,x10
00c9beb4  cmp x2,#0x3f0
00c9beb8  b.le 0x00c9c4d8
00c9bebc  cbz x11,0x00c9becc
00c9bec0  cbz x12,0x00c9c0b8
00c9bec4  cbnz x11,0x00c9c464
00c9bec8  b 0x00c9be98
00c9becc  ldp q14,q15,[x10]
00c9bed0  fcmgt v14.2D,v13.2D,v14.2D
00c9bed4  ldp q1,q2,[x10, #0x20]
00c9bed8  fcmgt v15.2D,v13.2D,v15.2D
00c9bedc  bic v14.16B,v5.16B,v14.16B
00c9bee0  fcmgt v1.2D,v13.2D,v1.2D
00c9bee4  bic v15.16B,v6.16B,v15.16B
00c9bee8  fcmgt v2.2D,v13.2D,v2.2D
00c9beec  ldr q0,[sp, #0x40]
00c9bef0  ldp q3,q4,[x10, #0x40]
00c9bef4  bic v1.16B,v7.16B,v1.16B
00c9bef8  orr v14.16B,v15.16B,v14.16B
00c9befc  bic v2.16B,v16.16B,v2.16B
00c9bf00  orr v1.16B,v2.16B,v1.16B
00c9bf04  fcmgt v2.2D,v13.2D,v3.2D
00c9bf08  orr v1.16B,v1.16B,v14.16B
00c9bf0c  ldp q3,q14,[x10, #0x60]
00c9bf10  fcmgt v4.2D,v13.2D,v4.2D
00c9bf14  bic v2.16B,v17.16B,v2.16B
00c9bf18  fcmgt v3.2D,v13.2D,v3.2D
00c9bf1c  bic v4.16B,v18.16B,v4.16B
00c9bf20  orr v2.16B,v4.16B,v2.16B
00c9bf24  fcmgt v14.2D,v13.2D,v14.2D
00c9bf28  bic v3.16B,v19.16B,v3.16B
00c9bf2c  orr v2.16B,v3.16B,v2.16B
00c9bf30  ldp q4,q3,[x10, #0x80]
00c9bf34  orr v1.16B,v2.16B,v1.16B
00c9bf38  bic v2.16B,v20.16B,v14.16B
00c9bf3c  fcmgt v4.2D,v13.2D,v4.2D
00c9bf40  ldp q14,q15,[x10, #0xa0]
00c9bf44  fcmgt v3.2D,v13.2D,v3.2D
00c9bf48  bic v4.16B,v21.16B,v4.16B
00c9bf4c  orr v2.16B,v4.16B,v2.16B
00c9bf50  fcmgt v14.2D,v13.2D,v14.2D
00c9bf54  bic v3.16B,v22.16B,v3.16B
00c9bf58  orr v2.16B,v3.16B,v2.16B
00c9bf5c  bic v3.16B,v23.16B,v14.16B
00c9bf60  orr v2.16B,v3.16B,v2.16B
00c9bf64  ldp q4,q3,[x10, #0xc0]
00c9bf68  fcmgt v14.2D,v13.2D,v15.2D
00c9bf6c  orr v1.16B,v2.16B,v1.16B
00c9bf70  fcmgt v4.2D,v13.2D,v4.2D
00c9bf74  bic v2.16B,v24.16B,v14.16B
00c9bf78  fcmgt v3.2D,v13.2D,v3.2D
00c9bf7c  bic v4.16B,v25.16B,v4.16B
00c9bf80  orr v2.16B,v4.16B,v2.16B
00c9bf84  ldp q14,q4,[x10, #0xe0]
00c9bf88  bic v3.16B,v26.16B,v3.16B
00c9bf8c  orr v2.16B,v3.16B,v2.16B
00c9bf90  fcmgt v14.2D,v13.2D,v14.2D
00c9bf94  fcmgt v4.2D,v13.2D,v4.2D
00c9bf98  bic v3.16B,v27.16B,v14.16B
00c9bf9c  orr v2.16B,v3.16B,v2.16B
00c9bfa0  bic v3.16B,v28.16B,v4.16B
00c9bfa4  ldp q14,q4,[x10, #0x100]
00c9bfa8  orr v2.16B,v3.16B,v2.16B
00c9bfac  orr v1.16B,v2.16B,v1.16B
00c9bfb0  fcmgt v14.2D,v13.2D,v14.2D
00c9bfb4  fcmgt v3.2D,v13.2D,v4.2D
00c9bfb8  bic v2.16B,v29.16B,v14.16B
00c9bfbc  ldp q4,q14,[x10, #0x120]
00c9bfc0  bic v3.16B,v30.16B,v3.16B
00c9bfc4  orr v2.16B,v3.16B,v2.16B
00c9bfc8  fcmgt v4.2D,v13.2D,v4.2D
00c9bfcc  fcmgt v3.2D,v13.2D,v14.2D
00c9bfd0  bic v4.16B,v31.16B,v4.16B
00c9bfd4  orr v2.16B,v4.16B,v2.16B
00c9bfd8  ldp q14,q4,[x10, #0x140]
00c9bfdc  bic v3.16B,v8.16B,v3.16B
00c9bfe0  orr v2.16B,v3.16B,v2.16B
00c9bfe4  fcmgt v14.2D,v13.2D,v14.2D
00c9bfe8  fcmgt v4.2D,v13.2D,v4.2D
00c9bfec  bic v3.16B,v9.16B,v14.16B
00c9bff0  orr v2.16B,v3.16B,v2.16B
00c9bff4  bic v3.16B,v10.16B,v4.16B
00c9bff8  ldp q14,q4,[x10, #0x160]
00c9bffc  orr v2.16B,v3.16B,v2.16B
00c9c000  orr v1.16B,v2.16B,v1.16B
00c9c004  fcmgt v14.2D,v13.2D,v14.2D
00c9c008  fcmgt v3.2D,v13.2D,v4.2D
00c9c00c  bic v2.16B,v11.16B,v14.16B
00c9c010  ldp q4,q14,[x10, #0x180]
00c9c014  bic v3.16B,v12.16B,v3.16B
00c9c018  orr v2.16B,v3.16B,v2.16B
00c9c01c  fcmgt v4.2D,v13.2D,v4.2D
00c9c020  fcmgt v3.2D,v13.2D,v14.2D
00c9c024  bic v4.16B,v0.16B,v4.16B
00c9c028  ldr q0,[sp, #0x30]
00c9c02c  orr v2.16B,v4.16B,v2.16B
00c9c030  ldp q14,q4,[x10, #0x1a0]
00c9c034  bic v3.16B,v0.16B,v3.16B
00c9c038  orr v2.16B,v3.16B,v2.16B
00c9c03c  fcmgt v14.2D,v13.2D,v14.2D
00c9c040  ldp q3,q15,[x10, #0x1c0]
00c9c044  fcmgt v4.2D,v13.2D,v4.2D
00c9c048  fcmgt v3.2D,v13.2D,v3.2D
00c9c04c  ldr q0,[sp, #0x20]
00c9c050  bic v14.16B,v0.16B,v14.16B
00c9c054  ldr q0,[sp, #0x10]
00c9c058  orr v2.16B,v14.16B,v2.16B
00c9c05c  ldr q14,[x13, #0x850]
00c9c060  bic v4.16B,v0.16B,v4.16B
00c9c064  orr v2.16B,v4.16B,v2.16B
00c9c068  bic v3.16B,v14.16B,v3.16B
00c9c06c  fcmgt v14.2D,v13.2D,v15.2D
00c9c070  ldp q4,q15,[x10, #0x1e0]
00c9c074  orr v2.16B,v3.16B,v2.16B
00c9c078  orr v1.16B,v2.16B,v1.16B
00c9c07c  fcmgt v4.2D,v13.2D,v4.2D
00c9c080  ldr q3,[x14, #0x100]
00c9c084  ldr q2,[x15, #0xfb0]
00c9c088  fcmgt v15.2D,v13.2D,v15.2D
00c9c08c  bic v3.16B,v3.16B,v14.16B
00c9c090  ldr q14,[x16, #0xf50]
00c9c094  bic v2.16B,v2.16B,v4.16B
00c9c098  orr v2.16B,v2.16B,v3.16B
00c9c09c  bic v3.16B,v14.16B,v15.16B
00c9c0a0  orr v2.16B,v3.16B,v2.16B
00c9c0a4  orr v1.16B,v2.16B,v1.16B
00c9c0a8  ext v2.16B,v1.16B,v1.16B,0x8
00c9c0ac  orr v1.8B,v1.8B,v2.8B
00c9c0b0  fmov x11,d1
00c9c0b4  cbnz x12,0x00c9bec4
00c9c0b8  ldur q1,[x8, #-0x8]
00c9c0bc  sub x12,x8,#0x108
00c9c0c0  ldur q2,[x8, #-0x18]
00c9c0c4  ldur q4,[x8, #-0x38]
00c9c0c8  ldur q3,[x8, #-0x28]
00c9c0cc  ext v1.16B,v1.16B,v1.16B,0x8
00c9c0d0  ldur q14,[x8, #-0x48]
00c9c0d4  ext v2.16B,v2.16B,v2.16B,0x8
00c9c0d8  ldur q15,[x8, #-0x58]
00c9c0dc  ext v4.16B,v4.16B,v4.16B,0x8
00c9c0e0  ldr q0,[sp, #0x40]
00c9c0e4  ext v3.16B,v3.16B,v3.16B,0x8
00c9c0e8  fcmgt v1.2D,v13.2D,v1.2D
00c9c0ec  fcmgt v2.2D,v13.2D,v2.2D
00c9c0f0  fcmgt v4.2D,v13.2D,v4.2D
00c9c0f4  fcmgt v3.2D,v13.2D,v3.2D
00c9c0f8  ext v14.16B,v14.16B,v14.16B,0x8
00c9c0fc  and v1.16B,v1.16B,v5.16B
00c9c100  and v2.16B,v2.16B,v6.16B
00c9c104  orr v1.16B,v2.16B,v1.16B
00c9c108  and v2.16B,v4.16B,v16.16B
00c9c10c  ext v4.16B,v15.16B,v15.16B,0x8
00c9c110  ldur q15,[x8, #-0x68]
00c9c114  and v3.16B,v3.16B,v7.16B
00c9c118  orr v2.16B,v2.16B,v3.16B
00c9c11c  fcmgt v3.2D,v13.2D,v14.2D
00c9c120  ext v14.16B,v15.16B,v15.16B,0x8
00c9c124  ldur q15,[x8, #-0xd8]
00c9c128  fcmgt v4.2D,v13.2D,v4.2D
00c9c12c  orr v1.16B,v2.16B,v1.16B
00c9c130  and v2.16B,v3.16B,v17.16B
00c9c134  fcmgt v3.2D,v13.2D,v14.2D
00c9c138  ldur q14,[x8, #-0x78]
00c9c13c  and v4.16B,v4.16B,v18.16B
00c9c140  orr v2.16B,v4.16B,v2.16B
00c9c144  ext v4.16B,v14.16B,v14.16B,0x8
00c9c148  ldur q14,[x8, #-0x88]
00c9c14c  and v3.16B,v3.16B,v19.16B
00c9c150  orr v2.16B,v3.16B,v2.16B
00c9c154  ext v3.16B,v14.16B,v14.16B,0x8
00c9c158  ldur q14,[x8, #-0x98]
00c9c15c  orr v1.16B,v2.16B,v1.16B
00c9c160  fcmgt v4.2D,v13.2D,v4.2D
00c9c164  ext v2.16B,v14.16B,v14.16B,0x8
00c9c168  ldur q14,[x8, #-0xa8]
00c9c16c  fcmgt v3.2D,v13.2D,v3.2D
00c9c170  ext v14.16B,v14.16B,v14.16B,0x8
00c9c174  fcmgt v2.2D,v13.2D,v2.2D
00c9c178  and v4.16B,v4.16B,v20.16B
00c9c17c  and v3.16B,v3.16B,v21.16B
00c9c180  orr v3.16B,v3.16B,v4.16B
00c9c184  fcmgt v4.2D,v13.2D,v14.2D
00c9c188  ldur q14,[x8, #-0xb8]
00c9c18c  and v2.16B,v2.16B,v22.16B
00c9c190  orr v2.16B,v2.16B,v3.16B
00c9c194  ldur q3,[x8, #-0xc8]
00c9c198  ext v14.16B,v14.16B,v14.16B,0x8
00c9c19c  and v4.16B,v4.16B,v23.16B
00c9c1a0  ext v3.16B,v3.16B,v3.16B,0x8
00c9c1a4  orr v2.16B,v4.16B,v2.16B
00c9c1a8  fcmgt v4.2D,v13.2D,v14.2D
00c9c1ac  ext v14.16B,v15.16B,v15.16B,0x8
00c9c1b0  ldur q15,[x8, #-0xf8]
00c9c1b4  fcmgt v3.2D,v13.2D,v3.2D
00c9c1b8  orr v1.16B,v2.16B,v1.16B
00c9c1bc  and v2.16B,v4.16B,v24.16B
00c9c1c0  ldur q4,[x8, #-0xe8]
00c9c1c4  fcmgt v14.2D,v13.2D,v14.2D
00c9c1c8  and v3.16B,v3.16B,v25.16B
00c9c1cc  ext v4.16B,v4.16B,v4.16B,0x8
00c9c1d0  orr v2.16B,v3.16B,v2.16B
00c9c1d4  and v3.16B,v14.16B,v26.16B
00c9c1d8  ext v14.16B,v15.16B,v15.16B,0x8
00c9c1dc  orr v2.16B,v3.16B,v2.16B
00c9c1e0  ldr q3,[x12]
00c9c1e4  sub x12,x8,#0x118
00c9c1e8  fcmgt v4.2D,v13.2D,v4.2D
00c9c1ec  fcmgt v14.2D,v13.2D,v14.2D
00c9c1f0  ldr q15,[x12]
00c9c1f4  sub x12,x8,#0x128
00c9c1f8  ext v3.16B,v3.16B,v3.16B,0x8
00c9c1fc  and v4.16B,v4.16B,v27.16B
00c9c200  orr v2.16B,v4.16B,v2.16B
00c9c204  and v4.16B,v14.16B,v28.16B
00c9c208  ext v14.16B,v15.16B,v15.16B,0x8
00c9c20c  orr v2.16B,v4.16B,v2.16B
00c9c210  ldr q4,[x12]
00c9c214  sub x12,x8,#0x138
00c9c218  orr v1.16B,v2.16B,v1.16B
00c9c21c  fcmgt v2.2D,v13.2D,v3.2D
00c9c220  fcmgt v3.2D,v13.2D,v14.2D
00c9c224  ldr q14,[x12]
00c9c228  ext v4.16B,v4.16B,v4.16B,0x8
00c9c22c  sub x12,x8,#0x148
00c9c230  and v2.16B,v2.16B,v29.16B
00c9c234  and v3.16B,v3.16B,v30.16B
00c9c238  orr v2.16B,v3.16B,v2.16B
00c9c23c  ldr q3,[x12]
00c9c240  sub x12,x8,#0x158
00c9c244  fcmgt v4.2D,v13.2D,v4.2D
00c9c248  ext v14.16B,v14.16B,v14.16B,0x8
00c9c24c  ldr q15,[x12]
00c9c250  sub x12,x8,#0x168
00c9c254  ext v3.16B,v3.16B,v3.16B,0x8
00c9c258  and v4.16B,v4.16B,v31.16B
00c9c25c  orr v2.16B,v4.16B,v2.16B
00c9c260  ldr q4,[x12]
00c9c264  orr v1.16B,v2.16B,v1.16B
00c9c268  sub x12,x8,#0x178
00c9c26c  fcmgt v2.2D,v13.2D,v14.2D
00c9c270  ext v14.16B,v15.16B,v15.16B,0x8
00c9c274  ext v4.16B,v4.16B,v4.16B,0x8
00c9c278  ldr q15,[x12]
00c9c27c  fcmgt v3.2D,v13.2D,v3.2D
00c9c280  sub x12,x8,#0x188
00c9c284  and v2.16B,v2.16B,v8.16B
00c9c288  fcmgt v14.2D,v13.2D,v14.2D
00c9c28c  fcmgt v4.2D,v13.2D,v4.2D
00c9c290  and v3.16B,v3.16B,v9.16B
00c9c294  orr v2.16B,v3.16B,v2.16B
00c9c298  and v3.16B,v14.16B,v10.16B
00c9c29c  orr v2.16B,v3.16B,v2.16B
00c9c2a0  ldr q3,[x12]
00c9c2a4  sub x12,x8,#0x198
00c9c2a8  and v4.16B,v4.16B,v11.16B
00c9c2ac  ext v14.16B,v15.16B,v15.16B,0x8
00c9c2b0  orr v2.16B,v4.16B,v2.16B
00c9c2b4  ext v3.16B,v3.16B,v3.16B,0x8
00c9c2b8  orr v1.16B,v2.16B,v1.16B
00c9c2bc  ldr q2,[x12]
00c9c2c0  sub x12,x8,#0x1a8
00c9c2c4  fcmgt v4.2D,v13.2D,v14.2D
00c9c2c8  ext v2.16B,v2.16B,v2.16B,0x8
00c9c2cc  ldr q14,[x12]
00c9c2d0  sub x12,x8,#0x1b8
00c9c2d4  fcmgt v3.2D,v13.2D,v3.2D
00c9c2d8  and v4.16B,v4.16B,v12.16B
00c9c2dc  ext v14.16B,v14.16B,v14.16B,0x8
00c9c2e0  ldr q15,[x12]
00c9c2e4  fcmgt v2.2D,v13.2D,v2.2D
00c9c2e8  sub x12,x8,#0x1c8
00c9c2ec  and v3.16B,v3.16B,v0.16B
00c9c2f0  ldr q0,[sp, #0x30]
00c9c2f4  orr v3.16B,v3.16B,v4.16B
00c9c2f8  ext v4.16B,v15.16B,v15.16B,0x8
00c9c2fc  fcmgt v14.2D,v13.2D,v14.2D
00c9c300  and v2.16B,v2.16B,v0.16B
00c9c304  ldr q0,[sp, #0x20]
00c9c308  orr v2.16B,v2.16B,v3.16B
00c9c30c  fcmgt v3.2D,v13.2D,v4.2D
00c9c310  and v4.16B,v14.16B,v0.16B
00c9c314  ldr q14,[x12]
00c9c318  sub x12,x8,#0x1d8
00c9c31c  ldr q0,[sp, #0x10]
00c9c320  orr v2.16B,v4.16B,v2.16B
00c9c324  ldr q4,[x12]
00c9c328  sub x12,x8,#0x1e8
00c9c32c  and v3.16B,v3.16B,v0.16B
00c9c330  orr v2.16B,v3.16B,v2.16B
00c9c334  ext v3.16B,v14.16B,v14.16B,0x8
00c9c338  ldr q14,[x12]
00c9c33c  sub x12,x8,#0x1f8
00c9c340  ext v4.16B,v4.16B,v4.16B,0x8
00c9c344  ext v14.16B,v14.16B,v14.16B,0x8
00c9c348  ldr q15,[x12]
00c9c34c  fcmgt v3.2D,v13.2D,v3.2D
00c9c350  orr v1.16B,v2.16B,v1.16B
00c9c354  ldr q2,[x13, #0x850]
00c9c358  fcmgt v4.2D,v13.2D,v4.2D
00c9c35c  ext v15.16B,v15.16B,v15.16B,0x8
00c9c360  mov v0.16B,v12.16B
00c9c364  mov v12.16B,v11.16B
00c9c368  mov v11.16B,v10.16B
00c9c36c  mov v10.16B,v9.16B
00c9c370  mov v9.16B,v8.16B
00c9c374  mov v8.16B,v31.16B
00c9c378  mov v31.16B,v30.16B
00c9c37c  mov v30.16B,v29.16B
00c9c380  mov v29.16B,v28.16B
00c9c384  mov v28.16B,v27.16B
00c9c388  mov v27.16B,v26.16B
00c9c38c  mov v26.16B,v25.16B
00c9c390  mov v25.16B,v24.16B
00c9c394  mov v24.16B,v23.16B
00c9c398  mov v23.16B,v22.16B
00c9c39c  mov v22.16B,v21.16B
00c9c3a0  mov v21.16B,v20.16B
00c9c3a4  mov v20.16B,v19.16B
00c9c3a8  mov v19.16B,v18.16B
00c9c3ac  mov v18.16B,v17.16B
00c9c3b0  mov v17.16B,v16.16B
00c9c3b4  mov v16.16B,v7.16B
00c9c3b8  mov v7.16B,v6.16B
00c9c3bc  mov v6.16B,v5.16B
00c9c3c0  ldr q5,[x14, #0x100]
00c9c3c4  and v2.16B,v3.16B,v2.16B
00c9c3c8  fcmgt v3.2D,v13.2D,v14.2D
00c9c3cc  and v4.16B,v4.16B,v5.16B
00c9c3d0  ldr q5,[x15, #0xfb0]
00c9c3d4  fcmgt v14.2D,v13.2D,v15.2D
00c9c3d8  orr v2.16B,v4.16B,v2.16B
00c9c3dc  ldr q4,[x16, #0xf50]
00c9c3e0  and v3.16B,v3.16B,v5.16B
00c9c3e4  orr v2.16B,v3.16B,v2.16B
00c9c3e8  and v3.16B,v14.16B,v4.16B
00c9c3ec  orr v2.16B,v3.16B,v2.16B
00c9c3f0  orr v1.16B,v2.16B,v1.16B
00c9c3f4  ext v2.16B,v1.16B,v1.16B,0x8
00c9c3f8  mov v5.16B,v6.16B
00c9c3fc  mov v6.16B,v7.16B
00c9c400  mov v7.16B,v16.16B
00c9c404  orr v1.8B,v1.8B,v2.8B
00c9c408  fmov x12,d1
00c9c40c  mov v16.16B,v17.16B
00c9c410  mov v17.16B,v18.16B
00c9c414  mov v18.16B,v19.16B
00c9c418  mov v19.16B,v20.16B
00c9c41c  mov v20.16B,v21.16B
00c9c420  mov v21.16B,v22.16B
00c9c424  mov v22.16B,v23.16B
00c9c428  mov v23.16B,v24.16B
00c9c42c  mov v24.16B,v25.16B
00c9c430  mov v25.16B,v26.16B
00c9c434  mov v26.16B,v27.16B
00c9c438  mov v27.16B,v28.16B
00c9c43c  mov v28.16B,v29.16B
00c9c440  mov v29.16B,v30.16B
00c9c444  mov v30.16B,v31.16B
00c9c448  mov v31.16B,v8.16B
00c9c44c  mov v8.16B,v9.16B
00c9c450  mov v9.16B,v10.16B
00c9c454  mov v10.16B,v11.16B
00c9c458  mov v11.16B,v12.16B
00c9c45c  mov v12.16B,v0.16B
00c9c460  cbz x11,0x00c9be98
00c9c464  cbz x12,0x00c9be98
00c9c468  rbit x2,x11
00c9c46c  rbit x3,x12
00c9c470  clz x2,x2
00c9c474  clz x3,x3
00c9c478  lsl x2,x2,#0x3
00c9c47c  sub x4,x11,#0x1
00c9c480  sub x3,x8,x3, LSL #0x3
00c9c484  and x11,x4,x11
00c9c488  sub x4,x12,#0x1
00c9c48c  ldr d1,[x10,x2]
00c9c490  and x12,x4,x12
00c9c494  ldr d2,[x3]
00c9c498  str d2,[x10,x2]
00c9c49c  str d1,[x3]
00c9c4a0  cbz x11,0x00c9be98
00c9c4a4  cbnz x12,0x00c9c468
00c9c4a8  b 0x00c9be98
00c9c4ac  mov x11,xzr
00c9c4b0  mov x12,xzr
00c9c4b4  mov x14,xzr
00c9c4b8  asr x13,x2,#0x3
00c9c4bc  cbz x14,0x00c9c4e8
00c9c4c0  sub x13,x13,#0x3f
00c9c4c4  mov w15,#0x40
00c9c4c8  mov w14,#0x40
00c9c4cc  cbz x11,0x00c9c500
00c9c4d0  cbnz x12,0x00c9c6bc
00c9c4d4  b 0x00c9c5dc
00c9c4d8  ldr q0,[sp]
00c9c4dc  orr x14,x11,x12
00c9c4e0  asr x13,x2,#0x3
00c9c4e4  cbnz x14,0x00c9c4c0
00c9c4e8  add x11,x13,#0x1
00c9c4ec  add x14,x13,#0x2
00c9c4f0  cmp x11,#0x0
00c9c4f4  csinc x13,x14,x13,lt
00c9c4f8  asr x13,x13,#0x1
00c9c4fc  sub x15,x11,x13
00c9c500  cmp x13,#0x1
00c9c504  b.lt 0x00c9c520
00c9c508  cmp x13,#0x4
00c9c50c  b.cs 0x00c9c528
00c9c510  mov x14,xzr
00c9c514  mov x11,xzr
00c9c518  mov x16,x10
00c9c51c  b 0x00c9c5b0
00c9c520  mov x11,xzr
00c9c524  b 0x00c9c5d0
00c9c528  adrp x17,0x3b0000
00c9c52c  and x14,x13,#-0x4
00c9c530  mov w2,#0x2
00c9c534  mov w3,#0x1
00c9c538  mov w4,#0x4
00c9c53c  add x11,x10,#0x10
00c9c540  movi v2.2D,#0x0
00c9c544  add x16,x10,x14, LSL #0x3
00c9c548  movi v4.2D,#0x0
00c9c54c  ldr q3,[x17, #0x4f0]
00c9c550  mov x17,x14
00c9c554  dup v1.2D,v0.D[0x0]
00c9c558  dup v5.2D,x2
00c9c55c  dup v6.2D,x3
00c9c560  dup v7.2D,x4
00c9c564  ldp q16,q17,[x11, #-0x10]
00c9c568  add v18.2D,v3.2D,v5.2D
00c9c56c  add x11,x11,#0x20
00c9c570  subs x17,x17,#0x4
00c9c574  fcmgt v16.2D,v1.2D,v16.2D
00c9c578  fcmgt v17.2D,v1.2D,v17.2D
00c9c57c  bic v16.16B,v6.16B,v16.16B
00c9c580  ushl v16.2D,v16.2D,v3.2D
00c9c584  bic v17.16B,v6.16B,v17.16B
00c9c588  ushl v17.2D,v17.2D,v18.2D
00c9c58c  add v3.2D,v3.2D,v7.2D
00c9c590  orr v2.16B,v16.16B,v2.16B
00c9c594  orr v4.16B,v17.16B,v4.16B
00c9c598  b.ne 0x00c9c564
00c9c59c  orr v1.16B,v4.16B,v2.16B
00c9c5a0  ext v2.16B,v1.16B,v1.16B,0x8
00c9c5a4  orr v1.8B,v1.8B,v2.8B
00c9c5a8  fmov x11,d1
00c9c5ac  b 0x00c9c5c8
00c9c5b0  ldr d1,[x16], #0x8
00c9c5b4  fcmp d1,d0
00c9c5b8  cset w17,pl
00c9c5bc  lsl x17,x17,x14
00c9c5c0  add x14,x14,#0x1
00c9c5c4  orr x11,x17,x11
00c9c5c8  cmp x13,x14
00c9c5cc  b.ne 0x00c9c5b0
00c9c5d0  mov x14,x13
00c9c5d4  mov x13,x15
00c9c5d8  cbnz x12,0x00c9c6bc
00c9c5dc  cmp x13,#0x1
00c9c5e0  b.lt 0x00c9c5fc
00c9c5e4  cmp x13,#0x4
00c9c5e8  b.cs 0x00c9c60c
00c9c5ec  mov x15,xzr
00c9c5f0  mov x12,xzr
00c9c5f4  mov x16,x8
00c9c5f8  b 0x00c9c69c
00c9c5fc  cmp x11,#0x0
00c9c600  csel x12,x14,xzr,eq
00c9c604  add x10,x10,x12, LSL #0x3
00c9c608  b 0x00c9c758
00c9c60c  adrp x17,0x3b0000
00c9c610  and x15,x13,#-0x4
00c9c614  mov w2,#0x2
00c9c618  mov w3,#0x1
00c9c61c  mov w4,#0x4
00c9c620  sub x12,x8,#0x8
00c9c624  movi v2.2D,#0x0
00c9c628  sub x16,x8,x15, LSL #0x3
00c9c62c  movi v4.2D,#0x0
00c9c630  ldr q3,[x17, #0x4f0]
00c9c634  mov x17,x15
00c9c638  dup v1.2D,v0.D[0x0]
00c9c63c  dup v5.2D,x2
00c9c640  dup v6.2D,x3
00c9c644  dup v7.2D,x4
00c9c648  ldp q17,q16,[x12, #-0x10]
00c9c64c  add v18.2D,v3.2D,v5.2D
00c9c650  sub x12,x12,#0x20
00c9c654  subs x17,x17,#0x4
00c9c658  ext v17.16B,v17.16B,v17.16B,0x8
00c9c65c  ext v16.16B,v16.16B,v16.16B,0x8
00c9c660  fcmgt v17.2D,v1.2D,v17.2D
00c9c664  fcmgt v16.2D,v1.2D,v16.2D
00c9c668  and v17.16B,v17.16B,v6.16B
00c9c66c  ushl v17.2D,v17.2D,v18.2D
00c9c670  and v16.16B,v16.16B,v6.16B
00c9c674  ushl v16.2D,v16.2D,v3.2D
00c9c678  add v3.2D,v3.2D,v7.2D
00c9c67c  orr v2.16B,v16.16B,v2.16B
00c9c680  orr v4.16B,v17.16B,v4.16B
00c9c684  b.ne 0x00c9c648
00c9c688  orr v1.16B,v4.16B,v2.16B
00c9c68c  ext v2.16B,v1.16B,v1.16B,0x8
00c9c690  orr v1.8B,v1.8B,v2.8B
00c9c694  fmov x12,d1
00c9c698  b 0x00c9c6b4
00c9c69c  ldr d1,[x16], #-0x8
00c9c6a0  fcmp d1,d0
00c9c6a4  cset w17,mi
00c9c6a8  lsl x17,x17,x15
00c9c6ac  add x15,x15,#0x1
00c9c6b0  orr x12,x17,x12
00c9c6b4  cmp x13,x15
00c9c6b8  b.ne 0x00c9c69c
00c9c6bc  cbz x11,0x00c9c704
00c9c6c0  cbz x12,0x00c9c704
00c9c6c4  rbit x15,x11
00c9c6c8  rbit x16,x12
00c9c6cc  clz x15,x15
00c9c6d0  clz x16,x16
00c9c6d4  lsl x15,x15,#0x3
00c9c6d8  sub x17,x11,#0x1
00c9c6dc  sub x16,x8,x16, LSL #0x3
00c9c6e0  and x11,x17,x11
00c9c6e4  sub x17,x12,#0x1
00c9c6e8  ldr d1,[x10,x15]
00c9c6ec  and x12,x17,x12
00c9c6f0  ldr d2,[x16]
00c9c6f4  str d2,[x10,x15]
00c9c6f8  str d1,[x16]
00c9c6fc  cbz x11,0x00c9c704
00c9c700  cbnz x12,0x00c9c6c4
00c9c704  cmp x11,#0x0
00c9c708  csel x14,x14,xzr,eq
00c9c70c  add x10,x10,x14, LSL #0x3
00c9c710  cbz x12,0x00c9c758
00c9c714  cbnz x11,0x00c9c760
00c9c718  mov x11,#-0x1
00c9c71c  b 0x00c9c730
00c9c720  lsl x13,x11,x13
00c9c724  add x10,x10,#0x8
00c9c728  bic x12,x12,x13
00c9c72c  cbz x12,0x00c9c7a4
00c9c730  clz x13,x12
00c9c734  eor x13,x13,#0x3f
00c9c738  sub x14,x8,x13, LSL #0x3
00c9c73c  cmp x10,x14
00c9c740  b.eq 0x00c9c720
00c9c744  ldr d1,[x10]
00c9c748  ldr d2,[x14]
00c9c74c  str d1,[x14]
00c9c750  str d2,[x10]
00c9c754  b 0x00c9c720
00c9c758  cbz x11,0x00c9c7a4
00c9c75c  sub x8,x8,x13, LSL #0x3
00c9c760  mov x12,#-0x1
00c9c764  b 0x00c9c778
00c9c768  lsl x13,x12,x13
00c9c76c  sub x8,x8,#0x8
00c9c770  bic x11,x11,x13
00c9c774  cbz x11,0x00c9c7a0
00c9c778  clz x13,x11
00c9c77c  eor x13,x13,#0x3f
00c9c780  add x14,x10,x13, LSL #0x3
00c9c784  cmp x8,x14
00c9c788  b.eq 0x00c9c768
00c9c78c  ldr d1,[x8]
00c9c790  ldr d2,[x14]
00c9c794  str d1,[x14]
00c9c798  str d2,[x8]
00c9c79c  b 0x00c9c768
00c9c7a0  add x10,x8,#0x8
00c9c7a4  sub x8,x10,#0x8
00c9c7a8  cmp x8,x0
00c9c7ac  b.eq 0x00c9c7b8
00c9c7b0  ldr d1,[x8]
00c9c7b4  str d1,[x0]
00c9c7b8  ldp d9,d8,[sp, #0x80]
00c9c7bc  cmp x9,x1
00c9c7c0  mov x0,x8
00c9c7c4  ldp d11,d10,[sp, #0x70]
00c9c7c8  cset w1,cs
00c9c7cc  str d0,[x8]
00c9c7d0  ldp d13,d12,[sp, #0x60]
00c9c7d4  ldp d15,d14,[sp, #0x50]
00c9c7d8  add sp,sp,#0x90
00c9c7dc  ret

