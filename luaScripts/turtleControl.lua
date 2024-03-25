-- Import required modules
os.loadAPI("luaScripts/turtleUtils.lua")
os.loadAPI("luaScripts/httpUtils.lua")

-- Main function to control the turtle
local function main()
    while true do
        -- Check and refill fuel
        if not turtleUtils.checkAndRefillFuel() then
            print("Failed to refuel. Check fuel status.")
            return
        end

        -- Find a suitable mining spot
        local success = turtleUtils.findMiningSpot()
        if success then
            -- Set up and start mining operation
            turtleUtils.setupMiner()
            turtleUtils.startMining()

            -- Wait for mining to complete
            turtleUtils.waitForMiningComplete()

            -- Pick up the miner and move to a new location
            turtleUtils.pickUpMiner()
            print("Mining operation completed. Moving to a new location.")
        else
            print("Failed to find a suitable mining spot.")
        end

        -- Send turtle status to Flask app
        local status, err = httpUtils.sendStatus()
        if not status then
            print("Failed to send status to Flask app: " .. err)
        else
            print("Status sent to Flask app successfully.")
        end

        -- Sleep for a short duration before continuing
        os.sleep(10)
    end
end

-- Run the main function
main()