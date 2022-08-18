if {[molinfo top get numframes] > 1} {
    animate goto start
    animate delete beg 0 end 0 top
}
animate goto end
mol modstyle 0 0 Licorice 0.2 15 15
mol modselect 0 0 serial 1 to 82
mol addrep 0
mol modstyle 1 0 VDW 0.4 15
mol modselect 1 0 serial 9 1 27 28 19 11 48 49
display resetview
