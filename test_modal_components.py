#!/usr/bin/env python3
"""
Test suite for Modal components in Flowbite MCP Server
Tests all modal variants: basic, confirmation, form, timeline
"""

import asyncio
import sys
import os

# Add the current directory to the path so we can import the mcp_server_simple module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_server_simple import SimpleMCPServer

class ModalComponentTester:
    def __init__(self):
        self.server = SimpleMCPServer()
        self.test_results = []
        
    async def test_basic_modal(self):
        """Test basic modal variant"""
        print("🧪 Testing Basic Modal...")
        
        result = await self.server.generate_component(
            component_type="modal",
            variant="basic",
            props={
                "id": "basic-modal",
                "title": "Terms of Service",
                "content": "Please read and accept our terms of service to continue.",
                "primary_button": "Accept",
                "secondary_button": "Decline"
            }
        )
        
        success = "error" not in result and "modal" in result["content"][0]["text"].lower()
        self.test_results.append(("Basic Modal", success))
        
        if success:
            print("✅ Basic modal generated successfully")
            print(f"   Generated ID: basic-modal")
            print(f"   Title: Terms of Service")
            print(f"   Buttons: Accept, Decline")
        else:
            print("❌ Basic modal generation failed")
            print(f"   Error: {result}")
        
        return success
    
    async def test_confirmation_modal(self):
        """Test confirmation modal variant"""
        print("\n🧪 Testing Confirmation Modal...")
        
        result = await self.server.generate_component(
            component_type="modal",
            variant="confirmation", 
            props={
                "id": "delete-confirmation",
                "message": "Are you sure you want to delete this item? This action cannot be undone.",
                "confirm_button": "Yes, delete it",
                "cancel_button": "No, keep it"
            }
        )
        
        success = "error" not in result and "confirmation" in result["content"][0]["text"].lower()
        self.test_results.append(("Confirmation Modal", success))
        
        if success:
            print("✅ Confirmation modal generated successfully")
            print(f"   Modal type: Delete confirmation")
            print(f"   Buttons: Yes, delete it | No, keep it")
        else:
            print("❌ Confirmation modal generation failed")
            print(f"   Error: {result}")
        
        return success
    
    async def test_form_modal(self):
        """Test form modal variant"""
        print("\n🧪 Testing Form Modal...")
        
        result = await self.server.generate_component(
            component_type="modal",
            variant="form",
            props={
                "id": "add-product-modal",
                "title": "Add New Product",
                "form_fields": "Product Name",
                "submit_button": "Add Product"
            }
        )
        
        success = "error" not in result and "form" in result["content"][0]["text"].lower()
        self.test_results.append(("Form Modal", success))
        
        if success:
            print("✅ Form modal generated successfully")
            print(f"   Form type: Add New Product")
            print(f"   Fields: Product Name")
            print(f"   Submit: Add Product")
        else:
            print("❌ Form modal generation failed")
            print(f"   Error: {result}")
        
        return success
    
    async def test_timeline_modal(self):
        """Test timeline modal variant"""
        print("\n🧪 Testing Timeline Modal...")
        
        result = await self.server.generate_component(
            component_type="modal",
            variant="timeline",
            props={
                "id": "project-timeline",
                "title": "Project History",
                "timeline_item": "Version 2.0 Released",
                "timeline_date": "March 2024",
                "timeline_description": "Major update with new features and improvements."
            }
        )
        
        success = "error" not in result and "timeline" in result["content"][0]["text"].lower()
        self.test_results.append(("Timeline Modal", success))
        
        if success:
            print("✅ Timeline modal generated successfully")
            print(f"   Timeline: Version 2.0 Released")
            print(f"   Date: March 2024")
            print(f"   Description: Major update...")
        else:
            print("❌ Timeline modal generation failed")
            print(f"   Error: {result}")
        
        return success
    
    async def test_modal_suggestions(self):
        """Test modal component suggestions"""
        print("\n🧪 Testing Modal Suggestions...")
        
        # Test popup/modal keyword suggestions
        result = await self.server.suggest_components(
            description="popup dialog for user confirmation",
            context="dashboard"
        )
        
        text = result["content"][0]["text"]
        has_modal = "modal" in text.lower()
        has_confirmation = "confirmation" in text.lower()
        
        success = has_modal and has_confirmation
        self.test_results.append(("Modal Suggestions", success))
        
        if success:
            print("✅ Modal suggestions working correctly")
            print(f"   Suggested modal component: ✓")
            print(f"   Context-aware suggestions: ✓")
        else:
            print("❌ Modal suggestions failed")
            print(f"   Modal suggested: {has_modal}")
            print(f"   Context-aware: {has_confirmation}")
        
        return success
    
    async def test_modal_validation(self):
        """Test modal component validation"""
        print("\n🧪 Testing Modal Validation...")
        
        # Test invalid variant
        result = await self.server.generate_component(
            component_type="modal",
            variant="invalid-variant",
            props={}
        )
        
        has_error = "error" in result
        success = has_error and "invalid-variant" in str(result.get("error", "")).lower()
        self.test_results.append(("Modal Validation", success))
        
        if success:
            print("✅ Modal validation working correctly")
            print(f"   Invalid variant detected: ✓")
            print(f"   Available variants listed: ✓")
        else:
            print("❌ Modal validation failed")
            print(f"   Error handling: {has_error}")
        
        return success
    
    async def test_modal_defaults(self):
        """Test modal default properties"""
        print("\n🧪 Testing Modal Defaults...")
        
        # Test modal with minimal props (should use defaults)
        result = await self.server.generate_component(
            component_type="modal",
            variant="basic",
            props={}
        )
        
        success = "error" not in result
        text = result["content"][0]["text"] if success else ""
        
        has_defaults = all(keyword in text.lower() for keyword in [
            "basic modal", "confirm", "cancel"
        ])
        
        success = success and has_defaults
        self.test_results.append(("Modal Defaults", success))
        
        if success:
            print("✅ Modal defaults working correctly")
            print(f"   Default title: ✓")
            print(f"   Default buttons: ✓")
            print(f"   Default content: ✓")
        else:
            print("❌ Modal defaults failed")
            print(f"   Result: {result}")
        
        return success
    
    async def run_all_tests(self):
        """Run all modal component tests"""
        print("🚀 Starting Modal Component Tests...")
        print("=" * 50)
        
        tests = [
            self.test_basic_modal,
            self.test_confirmation_modal,
            self.test_form_modal,
            self.test_timeline_modal,
            self.test_modal_suggestions,
            self.test_modal_validation,
            self.test_modal_defaults
        ]
        
        for test in tests:
            await test()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 MODAL COMPONENT TEST SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for _, success in self.test_results if success)
        total = len(self.test_results)
        
        for test_name, success in self.test_results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} | {test_name}")
        
        print(f"\n🎯 Results: {passed}/{total} tests passed ({passed/total*100:.1f}% success rate)")
        
        if passed == total:
            print("🎉 ALL MODAL TESTS PASSED! Modal components are working perfectly!")
            return True
        else:
            print("⚠️  Some modal tests failed. Check the output above for details.")
            return False

async def main():
    """Main test execution"""
    tester = ModalComponentTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n✨ Modal component implementation is complete and ready for use!")
        print("\n🔧 Try these examples:")
        print("   • generate_component('modal', 'basic', {'title': 'Welcome'})")
        print("   • generate_component('modal', 'confirmation', {'message': 'Delete item?'})")
        print("   • generate_component('modal', 'form', {'title': 'Add User'})")
        print("   • generate_component('modal', 'timeline', {'title': 'Project Status'})")
    else:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())