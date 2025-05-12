# TGMCP - Telegram Model Context Protocol

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/240px-Telegram_logo.svg.png" alt="Telegram Logo" width="120"/>
  <br>
  <b>Connect AI agents with Telegram using MCP standard</b>
</div>

## 📖 Overview

TGMCP is a Python package that implements the [Model Context Protocol (MCP)](https://github.com/anthropics/anthropic-cookbook/tree/main/model_context_protocol) for Telegram. It allows AI agents to seamlessly interact with Telegram accounts, providing access to messaging, contacts, groups, media sharing, and more.

This package acts as a bridge between AI assistants and Telegram, enabling them to:
- Read and send messages
- Manage contacts and groups
- Handle media (images, documents, stickers, GIFs)
- Perform administrative functions
- Update profile information

All data is handled locally and securely through the Telegram API.

## ✨ Key Features

- **Chat Operations**: List chats, retrieve messages, send messages
- **Contact Management**: Add, delete, block/unblock, search contacts
- **Group Administration**: Create groups, add members, manage permissions
- **Media Handling**: Send/receive files, stickers, GIFs, voice messages
- **Profile Management**: Update profile info, privacy settings
- **Message Operations**: Forward, edit, delete, pin messages
- **Administrative Functions**: Promote/demote admins, ban users

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Telegram API credentials ([obtain here](https://my.telegram.org/auth))
- UV package installer (recommended)

### Install with UV (Recommended)
```bash
# Clone the repository
git clone https://github.com/OEvortex/tgmcp.git
cd tgmcp

# Install with UV
uv pip install -e .
```

### Traditional Install
```bash
# Clone the repository
git clone https://github.com/OEvortex/tgmcp.git
cd tgmcp

# Install with pip
pip install -e .
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in your project directory with your Telegram API credentials:

```
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_SESSION_NAME=your_session_name
# Optional: Use string session instead of file session
# TELEGRAM_SESSION_STRING=your_session_string
```

### MCP Configuration

To use TGMCP with other MCP-compatible applications, add it to your MCP configuration file:

```json
{
  "mcpServers": {
    "mcp-telegram": {
      "command": "tgmcp", /* use full path if client can't find the command (e.g. "/usr/local/bin/tgmcp"). See IMPORTANT section below for full path instructions. */
      "args": ["start"],
      "env": {
        "TELEGRAM_API_ID": "<your_api_id>",
        "TELEGRAM_API_HASH": "<your_api_hash>"
      }
    }
  }
}
```

**IMPORTANT**: To find the full path to the `tgmcp` command:
- Windows: `where tgmcp` in Command Prompt or `Get-Command tgmcp` in PowerShell
- macOS/Linux: `which tgmcp` in Terminal

## 🔍 Usage

### Run as MCP Server
```bash
python -m tgmcp
```

### Use in Your Code
```python
import asyncio
from tgmcp import client

async def main():
    # Connect to Telegram
    await client.start()
    
    # Get user info
    me = await client.get_me()
    print(f"Logged in as: {me.first_name} {getattr(me, 'last_name', '')}")
    
    # Send a message
    await client.send_message('username', 'Hello from TGMCP!')
    
    # Disconnect when done
    await client.disconnect()

asyncio.run(main())
```

## 🛠️ Tools Available

### Chat Tools
- `get_chats` - Get a paginated list of all your Telegram chats
- `list_chats` - List available chats with detailed metadata (users, groups, channels)
- `get_chat` - Get detailed information about a specific chat by ID
- `get_direct_chat_by_contact` - Find direct chats with a specific contact by name/username/phone
- `send_message` - Send a text message to any chat
- `archive_chat` - Archive a chat to reduce clutter
- `unarchive_chat` - Unarchive a previously archived chat
- `mute_chat` - Mute notifications for a specific chat
- `unmute_chat` - Unmute previously silenced chat notifications
- `get_invite_link` - Get an invite link for a group or channel
- `export_chat_invite` - Create and export a new chat invite link
- `join_chat_by_link` - Join a chat using an invite link
- `import_chat_invite` - Import a chat invite by hash code

### Contact Tools
- `list_contacts` - List all contacts in your Telegram account
- `search_contacts` - Search for contacts by name, username, or phone number
- `get_contact_ids` - Get all contact IDs in your account
- `get_contact_chats` - List all chats involving a specific contact
- `get_last_interaction` - Get the most recent messages with a contact
- `add_contact` - Add a new contact to your Telegram account
- `delete_contact` - Delete a contact from your address book
- `block_user` - Block a user by their user ID
- `unblock_user` - Unblock a previously blocked user
- `import_contacts` - Import a list of contacts in batch
- `export_contacts` - Export all contacts as a JSON string
- `get_blocked_users` - Get a list of all users you've blocked
- `resolve_username` - Resolve a username to a user or chat ID
- `search_public_chats` - Search for public chats, channels, or bots

### Message Tools
- `get_messages` - Get paginated messages from a specific chat
- `list_messages` - Retrieve messages with optional filters (search, date)
- `get_message_context` - See messages before and after a specific message
- `forward_message` - Forward a message from one chat to another
- `edit_message` - Edit a message you previously sent
- `delete_message` - Delete a message by ID
- `pin_message` - Pin an important message in a chat
- `unpin_message` - Unpin a previously pinned message
- `mark_as_read` - Mark all messages as read in a chat
- `reply_to_message` - Reply to a specific message in a chat
- `get_history` - Get full chat history up to a limit
- `search_messages` - Search for messages in a chat by text
- `get_pinned_messages` - Get all pinned messages in a chat

### Group & Channel Tools
- `create_group` - Create a new group and add initial members
- `create_channel` - Create a new channel or supergroup
- `invite_to_group` - Invite users to a group or channel
- `leave_chat` - Leave a group or channel
- `get_participants` - List all participants in a group or channel
- `edit_chat_title` - Change the title of a chat, group, or channel
- `edit_chat_photo` - Change the photo of a chat, group, or channel
- `delete_chat_photo` - Remove the photo from a chat
- `promote_admin` - Promote a user to admin with custom rights
- `demote_admin` - Remove admin status from a user
- `ban_user` - Ban a user from a group or channel
- `unban_user` - Unban a previously banned user
- `get_admins` - Get all admins in a group or channel
- `get_banned_users` - Get a list of all banned users
- `get_recent_actions` - View recent admin actions in a group

### Media Tools
- `send_file` - Send any file (document, photo, video) to a chat
- `download_media` - Download media from a message to local storage
- `get_media_info` - Get detailed information about media in a message
- `send_voice` - Send a voice message (OGG/OPUS format)
- `send_sticker` - Send a sticker to a chat
- `get_sticker_sets` - Get a list of available sticker sets
- `get_gif_search` - Search for GIFs by query term
- `send_gif` - Send a GIF to a chat by its document ID

### Profile Tools
- `get_me` - Get information about your own Telegram user
- `update_profile` - Update your profile information (name, bio)
- `set_profile_photo` - Set a new profile photo
- `delete_profile_photo` - Delete your current profile photo
- `get_privacy_settings` - View your privacy settings
- `set_privacy_settings` - Update privacy settings (last seen, phone, etc.)
- `get_user_photos` - Get profile photos of any user
- `get_user_status` - Check a user's online status
- `get_bot_info` - Get information about a bot
- `set_bot_commands` - Set commands for bots you own

### Admin Tools
- `promote_admin` - Promote a user to admin in a group/channel
- `demote_admin` - Demote a user from admin status
- `ban_user` - Ban a user from a group or channel
- `unban_user` - Unban a previously banned user
- `get_admins` - Get all admins in a group or channel
- `get_banned_users` - Get all banned users in a group or channel
- `leave_chat` - Leave a group or channel
- `export_chat_invite` - Generate a new invite link
- `import_chat_invite` - Join a chat using an invite hash
- `get_recent_actions` - View recent administrative actions

## 📚 Example

```python
import asyncio
import os
from dotenv import load_dotenv
from tgmcp import client

# Load environment variables
load_dotenv()

async def example():
    # Start the client
    await client.start()
    
    # Get recent chats
    dialogs = await client.get_dialogs(limit=5)
    print("\nRecent chats:")
    for dialog in dialogs:
        chat_name = getattr(dialog.entity, "title", None) or getattr(dialog.entity, "first_name", "Unknown")
        print(f"- {chat_name} (ID: {dialog.entity.id})")
    
    # Disconnect when done
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(example())
```

## 🔒 Security & Privacy

- All data remains on your local machine
- Authentication with Telegram is handled securely
- No data is sent to third parties
- Session files should be kept secure

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License

[MIT License](LICENSE)

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

<div align="center">
  <p>Made with ❤️ for AI-assisted Telegram interaction</p>
</div>
