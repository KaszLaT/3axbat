from 3axbat import Client, AuthenticationError

def main():
    client = Client()
    
    u = input("ID/Username: ").strip()
    p = input("Password: ").strip()
    
    try:
        print("\n[*] Logging in...")
        client.login(u, p)
        print("[+] Login successful!")
        
        print("\n[*] Fetching profile...")
        profile = client.get_profile()
        print(f"    Nickname: {profile.nickname}")
        print(f"    UID: {profile.user_id}")
        print(f"    Level: {profile.level}")
        print(f"    Description: {profile.description}")
        
        print("\n[*] Fetching friends...")
        friends = client.get_friends()
        print(f"    Total friends: {len(friends)}")
        for f in friends[:5]: # Print first 5 friends
            print(f"    - {f.nickname} ({f.user_id}) [{f.status_text}]")
            
        print("\n[*] Fetching Bed Wars server (Game 1008)...")
        server = client.get_game_server(1008)
        print(f"    Server IP:Port: {server}")
        
        print("\n[+] All tests passed successfully!")
        
    except AuthenticationError as e:
        print(f"\n[-] Auth Error: {e}")
    except Exception as e:
        print(f"\n[-] Error: {e}")

if __name__ == "__main__":
    main()