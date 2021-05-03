--DECLARACIÓN DE FUNCIONES AUXILIARES

function serializeTable(val, name, skipnewlines, depth)
    skipnewlines = skipnewlines or false
    depth = depth or 0

    local tmp = string.rep(" ", depth)

    if name then tmp = tmp .. name .. " = " end

    if type(val) == "table" then
        tmp = tmp .. "{" .. (not skipnewlines and "\n" or "")

        for k, v in pairs(val) do
            tmp =  tmp .. serializeTable(v, k, skipnewlines, depth + 1) .. "," .. (not skipnewlines and "\n" or "")
        end

        tmp = tmp .. string.rep(" ", depth) .. "}"
    elseif type(val) == "number" then
        tmp = tmp .. tostring(val)
    elseif type(val) == "string" then
        tmp = tmp .. string.format("%q", val)
    elseif type(val) == "boolean" then
        tmp = tmp .. (val and "true" or "false")
    else
        tmp = tmp .. "\"[inserializeable datatype:" .. type(val) .. "]\""
    end

    return tmp
end

-- CÓDIGO 
--
if emu.paused() then
    emu.unpause()
end
emu.poweron()
emu.loadrom("..\\Mike Tyson's Punch-Out!! (Japan, USA) (Rev A).nes")

movie.play("C:\\Users\\icalc\\Documents\\TFG\\tfg_blackbox\\temp_movies\\movie0.fm2")

fin_alg=false
emu.speedmode("normal") -- Set the speed of the emulator
f_objetivo=0
pelicula_cargada=movie.active()

while not fin_alg do

    -- Execute instructions for FCEUX

    if pelicula_cargada then

        oponente=memory.readbyte(0x0001)
        --Si el oponente es distinto del primero, supondremos que hemos derrotado con éxito
        --al 1er enemigo con éxito
        if not (oponente==0) then
            f_objetivo=emu.framecount()
            fin_alg=true
        elseif  movie.mode()=="finished" then
            f_objetivo=emu.framecount() + 1000
            fin_alg=true
        end
        
    end
    emu.frameadvance() -- This essentially tells FCEUX to keep running
    if fin_alg then
        emu.pause()
        file=io.open("C:\\Users\\icalc\\Documents\\TFG\\tfg_blackbox\\output\\output.txt",'a')
        io.output(file)
        io.write(tostring(f_objetivo).."\n")
        io.close()
    end
 
 end