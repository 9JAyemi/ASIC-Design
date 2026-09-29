onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate /tb_mult/inp_a
add wave -noupdate /tb_mult/inp_b
add wave -noupdate /tb_mult/prod
add wave -noupdate /tb_mult/clk
add wave -noupdate /tb_mult/rst
add wave -noupdate /tb_mult/uut/inp_a
add wave -noupdate /tb_mult/uut/inp_b
add wave -noupdate /tb_mult/uut/prod
add wave -noupdate /tb_mult/uut/clk
add wave -noupdate /tb_mult/uut/rst
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {1000 ns} 0}
quietly wave cursor active 1
configure wave -namecolwidth 40
configure wave -valuecolwidth 64
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ns
update
WaveRestoreZoom {0 ns} {4932 ns}
