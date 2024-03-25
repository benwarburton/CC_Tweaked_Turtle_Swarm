-- Functions related to HTTP communication with the Flask app

local function getTurtlePosition()
    -- Assuming GPS is set up and working in the game
    local x, y, z = gps.locate()
    if not x then
        print("GPS location failed, using fallback coordinates.")
        return {x = 0, y = 0, z = 0} -- Fallback if GPS fails
    end
    return {x = x, y = y, z = z}
end

local function getTurtleInventory()
    local inventory = {}
    for slot = 1, 16 do -- Turtles have 16 inventory slots
        local itemDetail = turtle.getItemDetail(slot)
        if itemDetail then
            table.insert(inventory, {name = itemDetail.name, count = itemDetail.count})
        end
    end
    return inventory
end

local function getTurtleStatus()
    -- This is a simplified way to determine the turtle's status
    -- More complex logic might be needed for different tasks
    if turtle.isMining() then
        return "mining"
    elseif turtle.isMoving() then
        return "moving"
    else
        return "idle"
    end
end

function sendStatus()
    local httpAPI = "http://localhost:8080/api/update_turtle" -- Replace with your Flask app's domain and endpoint
    local turtleData = {
        position = getTurtlePosition(),
        inventory = getTurtleInventory(),
        status = getTurtleStatus()
    }

    -- Convert turtleData to JSON
    local jsonData = textutils.serializeJSON(turtleData)

    -- Send HTTP POST request with turtle status
    local response, err = http.post(httpAPI, jsonData, {["Content-Type"] = "application/json"})

    if not response then
        print("Failed to send status to Flask app: " .. tostring(err))
    else
        local responseBody = response.readAll()
        print("Status sent to Flask app successfully. Response: " .. responseBody)
        response.close()
    end
end